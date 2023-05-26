import argparse
from singularity.slurpy.wikipedia.parsers import *

def main(args):
    shard_count = args.shards
    shard_number = args.shard_no

    # Example usage:
    # file_path = '2023-04-22/enwiki-20230420-pages-articles.xml.bz2'  # Replace with the path to your Wikipedia XML dump
    file_path = args.input_file
    wiki_iterator = WikipediaArticleIterator(file_path, shard_count, shard_number)

    # Create the WikipediaTextGenerator with the WikipediaArticleIterator
    text_generator = WikipediaTextGenerator(wiki_iterator)

    # Create a BPE tokenizer
    tokenizer = Tokenizer(models.BPE())

    # Customize pre-tokenization and decoding steps
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=True)
    tokenizer.decoder = decoders.ByteLevel()

    # Train the tokenizer using the WikipediaTextGenerator
    trainer = trainers.BpeTrainer(
        vocab_size=30522,  # Adjust the vocabulary size as needed
        special_tokens=["[PAD]", "[UNK]", "[CLS]", "[SEP]", "[MASK]"],  # Add any special tokens you need
        min_frequency=2,
    )
    tokenizer.train_from_iterator(text_generator, trainer=trainer)

    # Save the trained tokenizer
    # tokenizer.save("bpe_tokenizer.json")
    tokenizer.save(f"bpe_tokenizer_{shard_number}.json")

if __name__ == '__main__':
        # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--shards', type=int, required=True, help='Total number of shards')
    parser.add_argument('--shard-no', type=int, required=True, help='Shard number for this instance (0-based)')
    parser.add_argument('--input-file', type=str, required=True, help='Path to the Wikipedia XML dump (bz2 format)')
    args = parser.parse_args()

    main(args)


