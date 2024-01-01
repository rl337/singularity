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

class TrainingSet:
    items: Dict[str, TrainingItem]
    filename: str

    def __init__(self, filename: str):
        self.items = {}
        self.filename = filename

    def add(self, item: TrainingItem) -> bool:
        item_str = str(item)
        if item_str in self.items:
            return False
        self.items[item_str] = item

    def write(self):
        content = io.BytesIO()
        for item_str in self.items:
            content.write(f"{item_str}\n".encode("utf-8"))
        content.seek(0)

        with tarfile.open(self.filename, "w:gz") as tar:
            info = tarfile.TarInfo(name="items.txt")
            info.size = content.getbuffer().nbytes
            tar.addfile(tarinfo=info, fileobj=content)
    

