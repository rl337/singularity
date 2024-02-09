import transformers
import tokenizers
import tokenizers.models
import typing

VOCAB_FILES_NAMES = {
    "vocab_file": "vocab.json",
    "merges_file": "merges.txt",
}

class TemplateTokenizer(transformers.PreTrainedTokenizer):
    vocab_files_names = VOCAB_FILES_NAMES
    tokenizer: tokenizers.Tokenizer

    def __init__(self, **kwargs):
        self.tokenizer = tokenizers.Tokenizer(tokenizers.models.BPE())
        transformers.PreTrainedTokenizer.__init__(self, **kwargs)


    def get_vocab(self) -> typing.Dict[str, int]:
       return self.tokenizer.get_vocab()
