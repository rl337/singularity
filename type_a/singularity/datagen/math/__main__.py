import io
import json
import random
import tarfile
import singularity.datagen.vocab

from typing import Dict

digits = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

digits_inv = { digits[x]: x for x in digits }

exceptions = {
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
}

exceptions_inv = { exceptions[x]: x for x in exceptions }

tens = {
    "ten": 1,
    "twenty": 2,
    "thirty": 3,
    "forty": 4,
    "fifty": 5,
    "sixty": 6,
    "seventy": 7,
    "eighty": 8,
    "ninety": 9
}

tens_inv = { tens[x]: x for x in tens }

powers = {
    "thousand": 1000,
    "million": 1000000,
    "billion": 1000000000,
    "trillion": 1000000000000,
}

powers_inv = { powers[x]:x for x in powers }
powers_sorted = sorted_keys = sorted(powers, key=powers.get, reverse=True)

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
    


class NumberIdentityItem(TrainingItem):
    
    def __init__(self, number: int, synonym: str):
        super(NumberIdentityItem, self).__init__(synonym, f"{synonym} means {number}", number)


class SpelledOutNumberItem(NumberIdentityItem):

    def __init__(self, number: int, use_final_and=False, use_tens_space=True, use_tens_dash=True, use_grouping_commas=True):
        super(SpelledOutNumberItem, self).__init__(
            number,
            generate_number_string(
                number,
                use_grouping_commas,
                use_final_and,
                use_tens_dash,
                use_tens_space
            )
        )

class FormattedNumberItem(NumberIdentityItem):

    def __init__(self, number: int):
        super(FormattedNumberItem, self).__init__(number, f"{number:,}")


def generate_3_digit_number(raw_number: int, use_final_and=False, use_tens_space=True, use_tens_dash=True):

    number = abs(raw_number)
    sign = False
    if number != raw_number:
        sign = True

    if number == 0 or number >= 1000:
        return None

    parts = []
    if sign:
        parts.append("negative")

    hundreds_digit = int(number / 100)
    tens_digit = int((number - hundreds_digit*100) / 10)
    ones_digit = int(number - hundreds_digit*100 - tens_digit*10)
    tens_number = number - hundreds_digit*100
    no_ones = False
    if hundreds_digit > 0:
        parts.append(f"{digits_inv[hundreds_digit]} hundred")

    if tens_digit > 0 and ones_digit > 0 and use_final_and:
        parts.append("and")
    
    if tens_digit > 0:
        if tens_number in exceptions_inv:
            parts.append(exceptions_inv[tens_number])
            no_ones = True
        else:
            result = tens_inv[tens_digit]
            if ones_digit > 0:
                if use_tens_space:
                    if use_tens_dash:
                        result = f"{result}-{digits_inv[ones_digit]}"
                    else:
                        result = f"{result} {digits_inv[ones_digit]}"
                else:
                        result = f"{result}{digits_inv[ones_digit]}"

                no_ones = True
            parts.append(result)

    if not no_ones and ones_digit > 0:
        parts.append(digits_inv[ones_digit])

    return " ".join(parts)


def generate_number_string(number: int, use_grouping_commas=True, use_final_and=False, use_tens_dash=True, use_tens_space=True):

    remainder = abs(number)
    if remainder > 999 * powers[powers_sorted[0]]:
        return None

    parts = []
    if remainder != number:
        parts.append("negative")
     

    for power in powers_sorted:
        power_value = powers[power]
        if remainder < power_value:
            continue
        
        qty = int(remainder / power_value)
        remainder = remainder - qty * power_value

        digits_str = generate_3_digit_number(qty, use_final_and, use_tens_dash, use_tens_space)
        parts.append(f"{digits_str} {power}")

    if remainder > 0:
         parts.append(generate_3_digit_number(remainder, use_final_and, use_tens_dash, use_tens_space))

    if use_grouping_commas:
        return ", ".join(parts)
    else:
        return " ".join(parts)


class NumbersTrainingSet(TrainingSet):
    rnd: random.Random

    def __init__(self, rnd: random.Random, filename: str):
        super(NumbersTrainingSet, self).__init__(filename)
        self.rnd = rnd
    
    def add_number(self, number: int):
        kwargs = {
            'use_grouping_commas': self.rnd.randint(0, 100) % 2 == 0,
            'use_final_and': self.rnd.randint(0, 100) % 2 == 0,
            'use_tens_space': self.rnd.randint(0, 100) % 2 == 0,
            'use_tens_dash': self.rnd.randint(0, 100) % 2 == 0
        }
        self.add(SpelledOutNumberItem(number, **kwargs))
        self.add(FormattedNumberItem(number))

    def add_random_number(self, min: int, max: int):
        number = self.rnd.randint(min, max)
        self.add_number(number)
    
def main():
    rnd = random.Random(1)

    # numbers = singularity.datagen.vocab.load("en", "numbers")
    trainingset = NumbersTrainingSet(rnd, "numbers.tgz")
    for i in range(-1000, 1000):
        trainingset.add_number(i)
    trainingset.write()


if __name__ == '__main__':
    main()
