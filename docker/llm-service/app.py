import argparse
import logging
import os.path
import json
import importlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

def create_generator(model_path):
    # Load the model from the specified path
    return pipeline('text-generation', model=model_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Parse command line arguments for model path
    parser = argparse.ArgumentParser(description='LLM Service')
    parser.add_argument('models_config', type=str, help='Path to the model config json')
    parser.add_argument('model_path', type=str, help='Path to the model directory')
    parser.add_argument('static_path', type=str, help='Path to static files for webapp')
    parser.add_argument('model', type=str, help='the name and commit hash of the model')
    args = parser.parse_args()

    # validate static content directory
    if not os.path.isdir(args.static_path):
        raise FileNotFoundError(f"static content path {args.static_path} does not exist")

    # validate that path to models.json exists
    if not os.path.isfile(args.models_config):
        raise FileNotFoundError(f"config path {args.models_config} does not exist")

    with open(args.models_config, 'r') as fp:
        models_config = json.load(fp)

    models_list = list(models_config.keys())
    if args.model not in models_list:
        raise ValueError(f"model {args.model} was not found in {models_list}")

    model_config = models_config[args.model]
    if "driver" not in model_config:
        raise ValueError(f"model {args.model} from {args.models_config} not configured with driver.")
    model_driver = model_config['driver']


    model_dir = os.path.join(args.model_path, args.model)
    if not os.path.isdir(model_dir):
        raise FileNotFoundError(f"model path {model_dir} does not exist")

    try:
        package_name = model_driver['package']
        class_name = model_driver['class']
        submodule = importlib.import_module(package_name)
        model_class = getattr(submodule, class_name)
        logging.info (f"{class_name} from {package_name} has been imported successfully.")
    except ModuleNotFoundError:
        raise ValueError(f"Could not load package {package_name}")
    except AttributeError:
        raise ValueError(f"Class named {class_name} not found in {package_name}.")

    logging.info(f"loading {model_class.__name__} from {model_dir}")
    model = model_class(model_dir)
    model.initialize_generator()

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    app.add_api_route(path="/generate/", endpoint=model.generate_text, methods=["POST"])
    app.mount("/", StaticFiles(directory=args.static_path, html=True), name="static")
    
    # Start the FastAPI app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
