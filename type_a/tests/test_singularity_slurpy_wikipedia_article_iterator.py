import unittest
import bz2
import os
from singularity.slurpy.wikipedia.parsers import WikipediaArticleIterator
import xml.etree.ElementTree as ET

class WikipediaArticleIteratorTests(unittest.TestCase):
    def create_xml_file(self, test_case):
        root = ET.Element('mediawiki')
        root.set('xmlns', 'http://www.mediawiki.org/xml/export-0.10/')
        root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        root.set('xsi:schemaLocation', 'http://www.mediawiki.org/xml/export-0.10/ http://www.mediawiki.org/xml/export-0.10.xsd')

        for entry in test_case['xml_entries']:
            page_elem = ET.SubElement(root, 'page')

            title_elem = ET.SubElement(page_elem, 'title')
            title_elem.text = entry['title']

            if 'id' in entry:
                id_elem = ET.SubElement(page_elem, 'id')
                id_elem.text = entry['id']

            text_elem = ET.SubElement(page_elem, 'text')
            text_elem.text = entry['text']

        xml_file_path = 'test_file.xml.bz2'
        with bz2.open(xml_file_path, 'wt', encoding='utf-8') as xml_file:
            xml_str = ET.tostring(root, encoding='unicode')
            xml_file.write(xml_str)

        return xml_file_path


    def remove_xml_file(self, xml_file_path):
        os.remove(xml_file_path)

    def test_iterating_through_articles(self):
        test_cases = [
            {
                'xml_entries': [
                    {'title': 'Article 1', 'text': 'Content 1'},
                    {'title': 'Article 2', 'text': 'Content 2'}
                ],
                'expected_articles': [
                    {
                        'title': 'Article 1',
                        'content': ['Content 1'],
                        'file_refs': None,
                        'id': None
                    },
                    {
                        'title': 'Article 2',
                        'content': ['Content 2'],
                        'file_refs': None,
                        'id': None
                    }
                ]
            },
            {
                'xml_entries': [
                    {'title': 'Article 1', 'text': 'Paragraph 1.\n\nParagraph 2.\n\nParagraph 3.'},
                    {'title': 'Article 2', 'text': 'First paragraph.\n\nSecond paragraph.\n\nThird paragraph.'}
                ],
                'expected_articles': [
                    {
                        'title': 'Article 1',
                        'content': ['Paragraph 1.', 'Paragraph 2.', 'Paragraph 3.'],
                        'file_refs': None,
                        'id': None
                    },
                    {
                        'title': 'Article 2',
                        'content': ['First paragraph.', 'Second paragraph.', 'Third paragraph.'],
                        'file_refs': None,
                        'id': None
                    }
                ]
            },
            {
                'xml_entries': [
                    {'title': 'Article 1', 'text': 'Content 1 with a [[File:example1.jpg]] file.', 'id': '123'},
                    {'title': 'Article 2', 'text': 'Content 2 with a [[File:example2.jpg]] file.', 'id': '456'}
                ],
                'expected_articles': [
                    {
                        'title': 'Article 1',
                        'content': ['Content 1 with a file.'],
                        'file_refs': ['example1.jpg'],
                        'id': '123'
                    },
                    {
                        'title': 'Article 2',
                        'content': ['Content 2 with a file.'],
                        'file_refs': ['example2.jpg'],
                        'id': '456'
                    }
                ]
            },
            {
                'xml_entries': [
                    {'title': 'Article 3', 'text': 'Content 3 with two files: [[File:example3.jpg]] and [[File:example4.jpg]].', 'id': '789'},
                    {'title': 'Article 4', 'text': 'Content 4 without any files.', 'id': '012'}
                ],
                'expected_articles': [
                    {
                        'title': 'Article 3',
                        'content': ['Content 3 with two files: and .'],
                        'file_refs': ['example3.jpg', 'example4.jpg'],
                        'id': '789'
                    },
                    {
                        'title': 'Article 4',
                        'content': ['Content 4 without any files.'],
                        'file_refs': None,
                        'id': '012'
                    }
                ]
            }
            # Add more test cases as needed
        ]

        for i, test_case in enumerate(test_cases):
            xml_file_path = self.create_xml_file(test_case)
            iterator = WikipediaArticleIterator(xml_file_path, 1, 0)

            for j, expected_article in enumerate(test_case['expected_articles']):
                article = next(iterator)
                self.assertEqual(article['title'], expected_article['title'])
                self.assertEqual(article['content'], expected_article['content'])
                self.assertEqual(article['id'], expected_article['id'])
                self.assertEqual(article.get('file_refs'), expected_article.get('file_refs'))

            with self.assertRaises(StopIteration):
                next(iterator)

            self.remove_xml_file(xml_file_path)

if __name__ == '__main__':
    unittest.main()
