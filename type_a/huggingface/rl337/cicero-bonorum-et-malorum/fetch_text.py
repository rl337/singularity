import os
import re
import html
from urllib.request import urlopen

def download_file(url, filename):
    if not os.path.exists(filename):
        with urlopen(url) as response:
            html_content = response.read().decode('ISO-8859-1')
            with open(filename, 'w', encoding='utf-8') as out_file:
                out_file.write(html_content)

def strip_html_and_markers(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        content = re.sub(r'<head>.*?</head>', '', content, flags=re.DOTALL)
        # Remove anchor tags (both upper and lower case) and their content
        content = re.sub(r'<a href=[^>]+>.*?</a>', '', content, flags=re.IGNORECASE | re.DOTALL)
        # Remove other HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        # Remove markers like [1] or [et]
        content = re.sub(r'\[.*?\]', '', content)
        # Remove empty brackets
        content = re.sub(r'\[\]', '', content)

        content = re.sub(r'\n[\s]*\n', '\n\n', content)
        content = re.sub(r'^[ \t]+', '\t', content, flags=re.MULTILINE)

        return html.unescape(content)

def main():
    urls = [
        'http://www.thelatinlibrary.com/cicero/fin1.shtml',
        'http://www.thelatinlibrary.com/cicero/fin2.shtml',
        'http://www.thelatinlibrary.com/cicero/fin3.shtml',
        'http://www.thelatinlibrary.com/cicero/fin4.shtml',
        'http://www.thelatinlibrary.com/cicero/fin5.shtml',
    ]

    filenames = [
        'fin1.shtml',
        'fin2.shtml',
        'fin3.shtml',
        'fin4.shtml',
        'fin5.shtml',
    ]
    target_filenames = [
        'fin1.txt',
        'fin2.txt',
        'fin3.txt',
        'fin4.txt',
        'fin5.txt',
    ]

    for url, filename, target_filename in zip(urls, filenames, target_filenames):
        download_file(url, filename)
        final_text = strip_html_and_markers(filename) + '\n'

        with open(target_filename, 'w', encoding='utf-8') as file:
            file.write(final_text)

if __name__ == "__main__":
    main()

