from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.decoders import ByteLevel as ByteLevelDecoder
from tokenizers.normalizers import NFD
import transformers
import typing

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
