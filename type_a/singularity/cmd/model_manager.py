import argparse
import json
import os
import requests
from transformers import AutoModel, AutoTokenizer

def get_model_version(model_name):
    response = requests.get(f"https://huggingface.co/api/models/{model_name}")
    if response.status_code == 200:
        model_info = response.json()
        return model_info.get("sha", "unknown_version")  # 'sha' is a commit hash
    return "unknown_version"

def download_model(model_name, version, model_dir):
    print(f"Downloading {model_name} (version: {version})...")
    model = AutoModel.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    model_path = os.path.join(model_dir, model_name, version)
    os.makedirs(model_path, exist_ok=True)
    
    model.save_pretrained(model_path)
    tokenizer.save_pretrained(model_path)
    print(f"Model {model_name} (version: {version}) saved to {model_path}")

def load_model_list(model_list_file):
    with open(model_list_file, 'r') as file:
        data = json.load(file)
        return data["models"]

def main(model_list_file, model_dir):
    models = load_model_list(model_list_file)
    for model_info in models:
        model_name = model_info["name"]
        version = get_model_version(model_name)
        model_path = os.path.join(model_dir, model_name, version)
        if not os.path.exists(model_path):
            download_model(model_name, version, model_dir)
        else:
            print(f"Model {model_name} (version: {version}) already exists at {model_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Model Downloader')
    parser.add_argument('model_list_file', type=str, help='Path to the model list JSON file')
    parser.add_argument('model_dir', type=str, help='Path to the directory where models should be stored')
    args = parser.parse_args()
    main(args.model_list_file, args.model_dir)

