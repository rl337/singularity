import unittest
import tempfile
import os
import os.path
import json

from singularity.models.tokenizers.ascii import new_tokenizer, save_pretrained_tokenizer
from transformers import PreTrainedTokenizerFast

class TestAsciiTokenizer(unittest.TestCase):

    def test_tokenize(self):
        tokenizer = new_tokenizer()
        with tempfile.TemporaryDirectory() as save_path:
            save_file = os.path.join(save_path, 'tokenizer.json')
            save_pretrained_tokenizer(save_file)

            loaded_tokenizer = PreTrainedTokenizerFast(tokenizer_file=save_file)

            test_cases = [
                ("123", [49, 50, 51]),                # ASCII values for '123'
                ("!@#", [33, 64, 35]),                # ASCII values for '!@#'
                ("hello", [104, 101, 108, 108, 111]),  # ASCII values for 'hello'
            ]

            for text, expected in test_cases:
                with self.subTest(text=text):
                    output = loaded_tokenizer.encode(text)
                    # decoded_string = .tokenizer.decode(output)
                    self.assertEqual(output, expected)

if __name__ == '__main__':
    unittest.main()

