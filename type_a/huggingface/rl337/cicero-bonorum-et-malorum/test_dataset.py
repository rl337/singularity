import sys
import json
import os.path
from datasets import load_dataset

def test_load_dataset(dataset_dir):
    # Load the dataset
    dataset = load_dataset(dataset_dir)

    # Perform basic checks
    print("Number of books in the dataset:", len(dataset))
    for split_name in dataset:
        print("Number of eaxmples in", split_name, ":", len(dataset[split_name]))
        print("First few examples in", split_name, ":", json.dumps(dataset[split_name][:5]))

if __name__ == "__main__":

    test_dataset_script = sys.argv[0]
    test_dataset_dir = os.path.dirname(test_dataset_script)
    test_load_dataset(test_dataset_dir)

