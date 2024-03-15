from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.decoders import ByteLevel as ByteLevelDecoder
from tokenizers.normalizers import NFD

import torch
import transformers
import typing
import os

VOCAB_FILES_NAMES = {
    "vocab_file": "vocab.json",
    "merges_file": "merges.txt",
}

unk = '<unk>'
unk_id = 256

def new_tokenizer_model():
    # ASCII printable characters (32 to 126) mapped to 0 to 94
    vocab = {chr(i): unk_id for i in range(0, 256)}
    for i in range(32, 127):
        vocab[chr(i)] = i
    vocab[unk] = unk_id

    return BPE(unk_token=unk, vocab=vocab, merges=[])

class AsciiTokenizer(transformers.PreTrainedTokenizer):
    vocab_files_names = VOCAB_FILES_NAMES
    tokenizer: Tokenizer

    def __init__(self, **kwargs):
        tokenizer = Tokenizer(new_tokenizer_model())
        tokenizer.normalizer = NFD()
        tokenizer.pre_tokenizer = Whitespace()
        tokenizer.decoder = ByteLevelDecoder()
        self.tokenizer = tokenizer
        transformers.PreTrainedTokenizer.__init__(self, **kwargs)

    def get_vocab(self) -> typing.Dict[str, int]:
       return self.tokenizer.get_vocab()
    
    def save_pretrained(self, save_directory):
        # Ensure the save directory exists
        if not os.path.exists(save_directory):
            os.makedirs(save_directory, exist_ok=True)
        # Save the tokenizer to the specified directory
        self.tokenizer.save(os.path.join(save_directory, "tokenizer.json"))

    def tokenize(self, text, one_hot_encode=False, **kwargs):
        # Call the parent class's tokenize method
        tokenized_output = super().tokenize(text, **kwargs)

        if one_hot_encode:
            # Perform one-hot encoding
            return self.to_one_hot(tokenized_output)
        else:
            return tokenized_output

    def to_one_hot(self, indices):
        # Assuming `indices` is a list of token IDs
        # Implement one-hot encoding here, taking into account the tokenizer's vocabulary size
        vocab_size = self.vocab_size
        # Example one-hot encoding logic
        one_hot_vectors = torch.zeros((len(indices), vocab_size), dtype=torch.float32)
        for i, index in enumerate(indices):
            one_hot_vectors[i, index] = 1.0
        return one_hot_vectors

    @classmethod
    def from_pretrained(cls, pretrained_model_name_or_path, *init_inputs, **kwargs):
        # Instantiate the tokenizer from a saved file
        tokenizer_instance = cls(*init_inputs, **kwargs)
        
        # if this path exists, overwrite default mappings with found mappings
        load_path = os.path.join(pretrained_model_name_or_path, "tokenizer.json")
        if os.path.exists(load_path):
            tokenizer_instance.tokenizer = Tokenizer.from_file(load_path)
        return tokenizer_instance
