---
task_categories:
- text-generation
language:
- la
pretty_name: Cicero's De finibus bonorum et malorum
---

# Cicero's De finibus bonorum et malorum

## Overview
This dataset contains the text from Cicero's "De finibus bonorum et malorum." It is intended for use in comparing different neural network architectures within the "Neural Network Evolution" project.

## Source
Texts are sourced from The Latin Library. [The Latin Library](http://www.thelatinlibrary.com/)

## Preprocessing
The dataset was prepared using a Python script for fetching and processing the text. The script ensures consistent formatting and encoding.

Formatting decision
- remove all text in html header
- remove all html tags and tag bodies for anchors
- remove any references in brackets.  ex: [1]
- remove any implicit text additions.  ex: [et]
- collapse newlines to two separating paragraphs
- standardize paragraph intent to one tab

See fetch_text.py for details.

## Structure of the Dataset
- Format: Plain text
- Encoding: UTF-8
- Size: Approximately 94,616 words and 638,272 characters across 5 books

## License
This dataset is released under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

