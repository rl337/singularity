import os
import os.path

from typing import List
from datasets import DatasetInfo, GeneratorBasedBuilder, SplitGenerator, Features, Value


FILE_PATHS = {
    "book1": "fin1.txt",
    "book2": "fin2.txt",
    "book3": "fin3.txt",
    "book4": "fin4.txt",
    "book5": "fin5.txt"
}

SPLIT_LISTS = {
    "train": ["book1", "book2", "book3", "book4"],
    "test": ["book5"],
}

class CiceroCompletionEvaluationDataset(GeneratorBasedBuilder):
 
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.book_dataset = CiceroDataset(**kwargs)
    
    def _concatenate_texts(dataset_dict):
        concatenated_text = ''
        for i in [5]:  
            for line in dataset_dict[f'book{i}']['text']:
                book_text = ''.join([char if ord(char) < 128 else ' ' for char in line])
                concatenated_text += f'\r{book_text}'
        return concatenated_text

    def _generate_sequences(self, text, sequence_length=5):
        sequences = []

        for i in range(len(text) - sequence_length):
            sequence = text[i:i+sequence_length-1]
            label = text[i+sequence_length-1]
            sequences.append((sequence, label, i))
        return sequences

    def _info(self):
        return DatasetInfo(
            features=Features({
                'book': Value('string'),
                'line_number': Value('int32'),
                'line_offset': Value('int32'),
                'text': Value('string'),
                'label': Value('string'),
            })
        )
    
    def _generate_examples(self, books: List[str], sequence_length: int):
        files_in_split = [ 
            (book_name, os.path.join(self.base_path, FILE_PATHS[book_name]))
            for book_name in books
        ]
        
        for book_name, filepath in files_in_split:
            with open(filepath, encoding='utf-8') as f:
                for line_number, line in enumerate(f, start=1):
                    for sequence, label, i in self._generate_sequences(line.strip(), sequence_length):
                        yield f'{book_name}_{line_number}_{i}', {
                            'book': book_name,
                            'line_number': line_number,
                            'line_offset': i,
                            'text': sequence,
                            'label': label,
                        }
    
    def _split_generators(self, dl_manager):

        sequence_lengths = [3, 4, 5]
        split_keys = [
            (split, sequence_length)
            for split in SPLIT_LISTS
            for sequence_length in sequence_lengths
        ]
        
        return [
            SplitGenerator(
                name=f"{split}.len{sequence_length}",
                gen_kwargs={
                    "books": SPLIT_LISTS[split],
                    "sequence_length": sequence_length
                }
            ) for (split, sequence_length) in split_keys
        ]

class CiceroDataset(GeneratorBasedBuilder):
    
    def _info(self):
        return DatasetInfo(
            features=Features({
                'book': Value('string'),
                'line_number': Value('int32'),
                'text': Value('string'),
            })
        )
    
    def _generate_examples(self, filepath):
        book_name = os.path.splitext(os.path.basename(filepath))[0]  # e.g., 'book1'
        with open(filepath, encoding='utf-8') as f:
            for line_number, line in enumerate(f, start=1):
                yield f'{book_name}_{line_number}', {
                    'book': book_name,
                    'line_number': line_number,
                    'text': line.strip()
                }
    
    def _split_generators(self, dl_manager):
        return [
            SplitGenerator(
                name=key,
                gen_kwargs={"filepath": os.path.join(self.base_path, FILE_PATHS[key])}
            ) for key in FILE_PATHS
        ]


