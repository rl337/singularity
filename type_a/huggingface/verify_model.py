import transformers
import argparse
import json
import sys
import os.path
import logging


def verify_model(model: str):

    config_path = os.path.join(model, 'config.json')
    config_json = {}
    with open(config_path) as fp:
        config_json = json.load(fp)
    logging.info(f"successfully parsed config file {config_path}")

    config = transformers.AutoConfig.from_pretrained(model, local_files_only=True, trust_remote_code=True)
    logging.info(f"loaded config: {config}")

    tokenizer_path = os.path.join(model, 'tokenizer_config.json')
    if os.path.exists(tokenizer_path):
        logging.info(f"Tokenizer config found: {tokenizer_path}")
        tokenizer = transformers.AutoTokenizer.from_pretrained(model, config=config, local_files_only=True, trust_remote_code=True)
        if tokenizer == None:
            logging.fatal("Could not load tokenizer")
        logging.info("Tokenizer successfully loaded")



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

    verify_model(args.model)
