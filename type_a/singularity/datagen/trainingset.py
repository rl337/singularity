import io
import json
import tarfile

from typing import Dict

class TrainingItem:
    text: str
    explanation: str
    expression: str

    def __init__(self, text: str, explanation: str, expression: str):
        self.text = text
        self.explanation = explanation
        self.expression = expression

    def __str__(self):
        return json.dumps({
            "text": self.text,
            "explanation": self.explanation,
            "expression": self.expression
        })

    def __repr__(self):
        return str(self)

    def as_json(self):
        return str(self)

    def for_gpt2(self):
        output = json.dumps({'expression': self.expression, 'explanation': self.explanation})
        return json.dumps(f'Input: {json.dumps(self.text)}\nOutput: {json.dumps(output)}')

class InvalidTrainingItemError(Exception):
    pass

class TrainingSet:
    items: Dict[str, TrainingItem]
    filename: str

    def __init__(self, filename: str):
        self.items = {}
        self.filename = filename

    def add(self, item: TrainingItem) -> bool:
        if item is None:
            return False

        if item.text == "":
            raise InvalidTrainingItemError(item)

        if item.explanation == "":
            raise InvalidTrainingItemError(item)

        if item.expression == "":
            raise InvalidTrainingItemError(item)
            
     
        item_str = str(item)
        if item_str in self.items:
            return False
        self.items[item_str] = item

    def write_with_formatter(self, formatter):
        content = io.BytesIO()
        for item_str in self.items:
            item = self.items[item_str]
            content.write(formatter(item).encode("utf-8"))
        content.seek(0)

        with tarfile.open(self.filename, "w:gz") as tar:
            info = tarfile.TarInfo(name="items.txt")
            info.size = content.getbuffer().nbytes
            tar.addfile(tarinfo=info, fileobj=content)

    def write(self):
        self.write_with_formatter(lambda item: f"{item}\n")

    def write_for_gpt2(self):
        self.write_with_formatter(lambda item: f"{item.for_gpt2()}\n")
    

