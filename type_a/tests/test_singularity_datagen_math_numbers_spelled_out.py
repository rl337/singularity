import unittest

from singularity.datagen.math.numbers.spelled_out import generate_number_string

class SpelledOutNumberTest(unittest.TestCase):

    def test_iterating_through_articles(self):
        test_cases = [
            {"number": 1, "expected": "one"},
            {"number": 0, "expected": "zero"},
            # Add more test cases as needed
        ]

        for i, test_case in enumerate(test_cases):
            actual = generate_number_string(test_case['number'])
            self.assertEqual(test_case['expected'], actual)

if __name__ == '__main__':
    unittest.main()
