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


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create the parser
parser = argparse.ArgumentParser(description="Train a model on a specified dataset.")

# Add arguments
parser.add_argument("base_model_dir", type=str, help="Directory containing the base model.")
parser.add_argument("dataset", type=str, help="path to or dataset from huggingface")
parser.add_argument("output_dir", type=str, help="Directory where the fine-tuned model will be written.")
#parser.add_argument("--validation_set", type=str, default=None, help="Optional tarball (.tgz) file containing the validation set.")
#parser.add_argument("--max_length", type=int, default=1024, help="max_length for the tokenizer")
parser.add_argument("--epochs", type=int, default=32, help="block size for the tokenizer")
#parser.add_argument("--batch_size", type=int, default=8, help="data loader batch size")

# Parse arguments
args = parser.parse_args()
# model_id = "rl337/cicero-ffn"
conf = AutoConfig.from_pretrained(args.base_model_dir, local_files_only=True, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(args.base_model_dir, config=conf, local_files_only=True, trust_remote_code=True)
dataset = load_dataset(args.dataset, trust_remote_code=True)

def concatenate_texts(dataset_dict):
    concatenated_text = ''
    for i in range(1, 4):  # Assuming books are named 'book1' to 'book4'
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
sequences_tensor = torch.stack([torch.tensor(seq, dtype=torch.float32) for seq in sequences_one_hot])
labels_tensor = torch.tensor(labels, dtype=torch.long)


dataset = TensorDataset(sequences_tensor, labels_tensor)
data_loader = DataLoader(dataset, batch_size=64, shuffle=True)

try:
    model = AutoModel.from_pretrained(args.base_model_dir, config=conf, local_files_only=True, trust_remote_code=True)
    logger.info(f"Loaded pre-trained model from {args.base_model_dir}")
except (OSError, ValueError) as e:
    logger.info(f"No pretrained weights found creating a fresh model from {args.base_model_dir}")
    model = AutoModel.from_config(conf, name_or_path=args.base_model_dir, local_files_only=True, trust_remote_code=True)


optimizer = AdamW(model.parameters(), lr=5e-5)  # Set up the optimizer
total_steps = len(data_loader) * args.epochs  # Total number of training steps

loss_function = nn.CrossEntropyLoss()

# Training loop
model.train()
for epoch in range(args.epochs):
    for batch in data_loader:
        batch_input, batch_labels = batch
        # inputs = inputs.to('cuda')
        # masks = masks.to('cuda')
        outputs = model(batch_input)
        loss = loss_function(outputs, batch_labels)  # Adjust this line as per your model's output and task

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    logger.info(f"completed epoch {epoch} of {args.epochs}")


# Save the fine-tuned model
model.save_pretrained(args.output_dir)
tokenizer.save_pretrained(args.output_dir)

