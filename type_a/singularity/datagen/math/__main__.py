import random
import singularity.datagen.vocab
from singularity.datagen import TrainingItem, TrainingSet
from singularity.datagen.math.numbers.spelled_out import generate_number_string


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

    range_size = 1000
    # ranges are (min, max, use_random)
    ranges = [
        (0, 1000, False), # main numbers
        (1000, 10000, True), # to ten thousand
        (10000, 100000, True), # to hundred thousand
        (100000, 1000000, True),  # to a million
        (1000000, 10000000, True), # to ten million
        (10000000, 100000000, True), # to 100 million
        (100000000, 1000000000, True), # to a bilion
        (1000000000, 10000000000, True), # to ten billion
        (10000000000, 100000000000, True), # to hundred billion
        (100000000000, 1000000000000, True),  # to a trillion
        (1000000000000, 10000000000000, True),  # to ten trillion
        (10000000000000, 100000000000000, True),  # to a hundred trillion
    ]

    # numbers = singularity.datagen.vocab.load("en", "numbers")
    trainingset = NumbersTrainingSet(rnd, "numbers.tgz")
    for (range_min, range_max, use_random) in ranges:
        if not use_random:
            for i in range(range_min, range_max):
                trainingset.add_number(i)
                trainingset.add_number(-i)
        else:
            for i in range(0, range_size):
                trainingset.add_random_number(-range_max, -range_min)
                trainingset.add_random_number(range_min, range_max)
    
    trainingset.write_for_gpt2()


if __name__ == '__main__':
    main()
