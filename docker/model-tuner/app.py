import argparse
import tarfile

from transformers import GPT2Tokenizer, GPT2LMHeadModel, get_linear_schedule_with_warmup
import torch
from torch.optim import AdamW
from torch.utils.data import Dataset, DataLoader


# Load your data into a suitable format (adjust according to your data)
class LoadedDataset(Dataset):
    def __init__(self, tokenizer, file_path, block_size=32):
        self.tokenizer = tokenizer
        self.inputs = []
        self.attn_masks = []
        # ... Load and preprocess data
        with tarfile.open(file_path, 'r:gz') as tgz:
            for member in tgz.getmembers():
                with tgz.extractfile(member) as file_obj:
                    for line_bytes in file_obj:
                        line = line_bytes.decode('utf-8').strip()
                        encoding = tokenizer(line, max_length=block_size, truncation=True, padding="max_length", return_tensors="pt")
                        self.inputs.append(encoding.input_ids.squeeze())  # Squeeze to remove batch dimension
                        self.attn_masks.append(encoding.attention_mask.squeeze())

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx):
        return self.inputs[idx], self.attn_masks[idx]


# Create the parser
parser = argparse.ArgumentParser(description="Train a model on a specified dataset.")

# Add arguments
parser.add_argument("base_model_dir", type=str, help="Directory containing the base model.")
parser.add_argument("training_set", type=str, help="Tarball (.tgz) file containing the training set.")
parser.add_argument("output_dir", type=str, help="Directory where the fine-tuned model will be written.")
parser.add_argument("--validation_set", type=str, default=None, help="Optional tarball (.tgz) file containing the validation set.")
parser.add_argument("--max_length", type=int, default=1024, help="max_length for the tokenizer")
parser.add_argument("--epochs", type=int, default=32, help="block size for the tokenizer")
parser.add_argument("--batch_size", type=int, default=8, help="data loader batch size")

# Parse arguments
args = parser.parse_args()

# Extract and load data
tokenizer = GPT2Tokenizer.from_pretrained(args.base_model_dir, local_files_only=True)
tokenizer.pad_token = tokenizer.eos_token

dataset = LoadedDataset(tokenizer, args.training_set)
data_loader = DataLoader(dataset, batch_size=args.batch_size)  # adjust batch size as needed

# Step 2: Fine Tune the Model
model = GPT2LMHeadModel.from_pretrained(args.base_model_dir, local_files_only=True)

if not torch.cuda.is_available():
    raise Exception("cuda is not avaiailable")
model = model.to('cuda')

optimizer = AdamW(model.parameters(), lr=5e-5)  # Set up the optimizer
total_steps = len(data_loader) * args.epochs  # Total number of training steps

# Training loop
model.train()
for epoch in range(args.epochs):
    for batch in data_loader:
        inputs, masks = batch
        outputs = model(inputs, attention_mask=masks, labels=inputs)
        loss = outputs.loss

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

# Save the fine-tuned model
model.save_pretrained(args.output_dir)

# Step 3: Load Fine-Tuned Model and Validate
# Load the fine-tuned model
# model = GPT2LMHeadModel.from_pretrained("path/to/save/model")
# model.eval()  # Set the model to evaluation mode

# Validation loop (similar to training loop but without backpropagation/updating model weights)
# ...

# Step 4: Summarize Performance
# Calculate and print out performance metrics
# ...


