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


if __name__ == '__main__':
        # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-file', type=str, required=True, help='Path to the Wikipedia XML dump (bz2 format)')
    args = parser.parse_args()

    main(args)


