import argparse
import bz2
from xml.etree.ElementTree import iterparse
import mwparserfromhell
from tokenizers import Tokenizer, trainers, models, pre_tokenizers, decoders
from typing import Iterator


def wikitext_to_plain_text(wikitext):
    parsed = mwparserfromhell.parse(wikitext)
    return parsed.strip_code()


class WikipediaArticleIterator:
    def __init__(self, file_path, shard_count, shard_number):
        self.xml_file = bz2.open(file_path, 'rt', encoding='utf-8')
        self.iter = iterparse(self.xml_file, events=('start', 'end'))
        self.title = None
        self.content = None
        self.plain_text_content = None
        self.article_id = None
        self.page_count = -1
        self.shard_count = shard_count
        self.shard_number = shard_number

    def __iter__(self):
        return self

    def __next__(self):
        for event, elem in self.iter:
            if event == 'start':
                if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}title':
                    self.title = elem.text
                elif elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}id' and self.article_id is None:
                    self.article_id = elem.text
            elif event == 'end':
                if elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}text':
                    self.content = elem.text
                elif elem.tag == '{http://www.mediawiki.org/xml/export-0.10/}page':
                    self.plain_text_content = wikitext_to_plain_text(self.content)
                    article_data = {
                        'title': self.title,
                        'content': self.plain_text_content,
                        'id': self.article_id
                    }
                    # Reset the title, content, and article_id
                    self.title = None
                    self.content = None
                    self.plain_text_content = None
                    self.article_id = None

                    # Clear the processed element to save memory
                    elem.clear()

                    self.page_count += 1
                    if self.page_count % self.shard_count != self.shard_number:
                        continue

                    return article_data
        # Close the file and raise StopIteration when the end of the file is reached
        self.xml_file.close()
        raise StopIteration


class WikipediaTextGenerator(Iterator):
    def __init__(self, wiki_iterator: WikipediaArticleIterator):
        self.wiki_iterator = wiki_iterator

    def __iter__(self):
        return self

    def __next__(self):
        article = next(self.wiki_iterator)
        if article is None:
            raise StopIteration
        print(article['title'])
        return article['content']
