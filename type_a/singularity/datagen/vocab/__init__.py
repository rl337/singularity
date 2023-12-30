from typing import Dict
import os.path 
import yaml

def get_resource_file(lang: str, name: str):
    # Get the directory of the current file (__init__.py)
    init_dir = os.path.dirname(__file__)
    
    # Construct the path to the file
    file_path = os.path.join(init_dir, lang, f"{name}.yaml")
    
    return file_path

def load(lang: str, name: str) -> Dict[str, Dict[str, str]]:
    filename = get_resource_file(lang, name)
    
    if not os.path.isfile(filename):
        raise FileNotFoundError(filename)

    with open(filename, "r") as fp:
        return yaml.safe_load(fp)
