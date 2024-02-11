import argparse
import json
import sys
import os.path
import logging
import tempfile
import shutil
import importlib

from typing import Tuple, Dict, Any

import transformers


def verify_config(model_id: str, model_path: str) -> Tuple[Dict[str, Any], transformers.PretrainedConfig]:
    config_path = os.path.join(model_path, 'config.json')
    config_json = {}
    with open(config_path) as fp:
        config_json = json.load(fp)
    logging.info(f"successfully parsed config file {config_path}")

    config = transformers.AutoConfig.from_pretrained(model_id, local_files_only=True, trust_remote_code=True)
    logging.info(f"loaded config: {config}")
  
    return config_json, config

def verify_tokenizer(model_id, model_path, config: transformers.PretrainedConfig) -> transformers.PreTrainedTokenizer:
    tokenizer_path = os.path.join(model_path, 'tokenizer_config.json')
    if os.path.exists(tokenizer_path):
        logging.info(f"Tokenizer config found: {tokenizer_path}")
        tokenizer = transformers.AutoTokenizer.from_pretrained(model_id, config=config, local_files_only=True, trust_remote_code=True)
        if tokenizer == None:
            logging.fatal("Could not load tokenizer")
        logging.info("Tokenizer successfully loaded")
        return tokenizer

def verify_model(model_id: str, storage_path: str = '.'):
    model_path = os.path.join(storage_path, model_id)
  
    config_json, config = verify_config(model_id, model_path)
    tokenizer = verify_tokenizer(model_id, model_path, config)

    if 'auto_map' not in config_json:
        logging.fatal("Model config does not have an auto_map")
    auto_map = config_json['auto_map']
    auto_map_keys = [auto_class for auto_class in auto_map.keys() if auto_class.startswith('AutoModel')]
    for auto_map_key in sorted(auto_map_keys):
        auto_class = getattr(transformers, auto_map_key)
        from_config_method = getattr(auto_class, 'from_config')
        from_pretrained_method = getattr(auto_class, 'from_pretrained')

        model_untrained = from_config_method(config, local_files_only=True, trust_remote_code=True)
        model_untrained.save_pretrained(save_directory=model_path)

        model = from_pretrained_method(model_path, config=config, local_files_only=True, trust_remote_code=True, use_safetensors=True)
        if model is None:
            logging.fatal("Could not load model")

def verify_model_in_tempdir(model_id: str):
    if not os.path.isdir(model_id):
        raise FileNotFoundError(model_id)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copytree(model_id, os.path.join(tmpdir, model_id))
        verify_model(model_id, tmpdir)


if __name__ == '__main__':
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    parser = argparse.ArgumentParser(description="Example script with debug option.")
    parser.add_argument("--model", type=str, help="model id (should correspond to a directory locally)", required=True)
    parser.add_argument("--debug", action="store_true", help="Enable debug mode", default=False)

    # Parse arguments
    args = parser.parse_args()

    if args.debug:
        # If an unhandled exception occurs, drop into pdb
        def info(type, value, tb):
            if hasattr(sys, 'ps1') or not sys.stderr.isatty():
                # We are in interactive mode or don't have a tty-like device, so we call the default hook
                sys.__excepthook__(type, value, tb)
            else:
                import traceback, pdb
                # We are NOT in interactive mode; print the exception...
                traceback.print_exception(type, value, tb)
                print("\n")
                # ...then start the debugger in post-mortem mode
                pdb.pm()
                
        sys.excepthook = info

    verify_model_in_tempdir(args.model)
