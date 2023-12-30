import json
from typing import Dict
import singularity.datagen.vocab


class TrainingItem:
    text: str
    explanation: str
    expression: str

    def __init__(self, text, explanation, expression):
        self.text = text
        self.explanation = explanation
        self.expression = expression

    def __str__(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.__str__()

class NumberIdentityItem(TrainingItem):
    
    def __init__(self, number, synonym):
        super(NumberIdentityItem, self).__init__(synonym, f"{synonym} means {number}", number)


def generate_number_identities(numbers: Dict[str,Dict[str,str]]):
    
    results = []
    for n in numbers:
        results += [ NumberIdentityItem(numbers[n][0], s) for s in numbers[n] ]

    return results
    
def main():
    numbers = singularity.datagen.vocab.load("en", "numbers")

    print(generate_number_identities(numbers))

    operations = singularity.datagen.vocab.load("en", "operations")


if __name__ == '__main__':
    main()
