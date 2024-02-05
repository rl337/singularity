import os
import json

from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.decoders import ByteLevel as ByteLevelDecoder
from tokenizers.normalizers import NFD, StripAccents


unk = '<unk>'
unk_id = 256

def new_tokenizer_model():
    # ASCII printable characters (32 to 126) mapped to 0 to 94
    vocab = {chr(i): unk_id for i in range(0, 256)}
    for i in range(32, 127):
        vocab[chr(i)] = i
    vocab[unk] = unk_id

    return BPE(unk_token=unk, vocab=vocab, merges=[])

def save_pretrained_tokenizer(save_path):
    tokenizer = Tokenizer(new_tokenizer_model())
    tokenizer.save(save_path)

def new_tokenizer():
    tokenizer = Tokenizer(new_tokenizer_model())

    tokenizer.normalizer = NFD()
    tokenizer.pre_tokenizer = Whitespace()
    tokenizer.decoder = ByteLevelDecoder()
    return tokenizer

