import sys
import argparse
import tarfile
import logging

from transformers import AutoConfig, AutoTokenizer, AutoModel
from torch.optim import AdamW
from datasets import load_dataset

import torch
from torch.utils.data import DataLoader, TensorDataset
import torch.nn as nn
from sklearn.metrics import accuracy_score, precision_recall_fscore_support


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create the parser
parser = argparse.ArgumentParser(description="evaluate a trained model on a specified dataset.")

# Add arguments
parser.add_argument("base_model_dir", type=str, help="Directory containing the base model.")
parser.add_argument("dataset", type=str, help="path to or dataset from huggingface")
parser.add_argument("--epochs", type=int, default=32, help="block size for the tokenizer")
parser.add_argument("--batch_size", type=int, default=8, help="data loader batch size")

# Parse arguments
args = parser.parse_args()
conf = AutoConfig.from_pretrained(args.base_model_dir, local_files_only=True, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(args.base_model_dir, config=conf, local_files_only=True, trust_remote_code=True)
dataset = load_dataset(args.dataset, trust_remote_code=True)

def concatenate_texts(dataset_dict):
    concatenated_text = ''
    for i in [5]:  
        for line in dataset_dict[f'book{i}']['text']:
            book_text = ''.join([char if ord(char) < 128 else ' ' for char in line])
            concatenated_text += f'\r{book_text}'
    return concatenated_text

def generate_sequences(text, sequence_length=5):
    sequences = []
    labels = []

    for i in range(len(text) - sequence_length):
        sequences.append(text[i:i+sequence_length-1])  # Input sequences (m-1 characters)
        labels.append(ord(text[i+sequence_length-1]))  # Target labels (the m-th character)

    return sequences, labels


def one_hot_encode(sequence):
    # Assuming sequence is a list of characters
    one_hot = torch.zeros((len(sequence), 256))  # Assuming ASCII
    for i, char in enumerate(sequence):
        index = ord(char)
        one_hot[i][index] = 1
    return one_hot

# Concatenate texts from the first four books
training_text = concatenate_texts(dataset)

# Generate sequences from the concatenated training text
sequences, labels = generate_sequences(training_text)
sequences_one_hot = [one_hot_encode(x) for x in sequences]
sequences_tensor = torch.stack([seq.clone().detach().to(dtype=torch.float32) for seq in sequences_one_hot])
labels_tensor = torch.tensor(labels, dtype=torch.long)


dataset = TensorDataset(sequences_tensor, labels_tensor)
data_loader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True)

model = None
try:
    model = AutoModel.from_pretrained(args.base_model_dir, config=conf, local_files_only=True, trust_remote_code=True)
except (OSError, ValueError) as e:
    logger.fatal("Couldn't load pretrained model", exc_info=1)
    sys.exit(-1)

total_steps = len(data_loader) * args.epochs  # Total number of training steps

# Placeholders for predictions and true labels
all_preds = []
all_true_labels = []

model.eval()
for batch in data_loader:
    inputs, labels = batch
    with torch.no_grad():  # Do not compute gradients during evaluation
        outputs = model(inputs)
        preds = torch.argmax(outputs, dim=-1)  # Assuming classification task
    
    all_preds.extend(preds.cpu().numpy())
    all_true_labels.extend(labels.cpu().numpy())

# Calculate metrics
accuracy = accuracy_score(all_true_labels, all_preds)
# Calculate macro-averaged precision and recall
precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(all_true_labels, all_preds, average='macro', zero_division=0)

# Calculate micro-averaged precision and recall
precision_micro, recall_micro, f1_micro, _ = precision_recall_fscore_support(all_true_labels, all_preds, average='micro', zero_division=0)

print(f"Macro-averaged Precision: {precision_macro}, Recall: {recall_macro}")
print(f"Micro-averaged Precision: {precision_micro}, Recall: {recall_micro}")

print(f"Accuracy: {accuracy}")

