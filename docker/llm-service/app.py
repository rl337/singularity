import argparse
import logging
import os.path
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from drivers import PipelineTextGeneratorDriver, Llama2TextGeneratorDriver, RedPajamaTextGeneratorDriver


def create_generator(model_path):
    # Load the model from the specified path
    return pipeline('text-generation', model=model_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Parse command line arguments for model path
    parser = argparse.ArgumentParser(description='LLM Service')
    parser.add_argument('model_config', type=str, help='Path to the model config json')
    parser.add_argument('model_path', type=str, help='Path to the model directory')
    parser.add_argument('static_path', type=str, help='Path to static files for webapp')
    parser.add_argument('model', type=str, help='the name and commit hash of the model')
    args = parser.parse_args()

    if not os.path.isfile(args.model_config):
        raise FileNotFoundError(f"config path {args.model_config} does not exist")
    with open(args.model_config, 'r') as fp:
        model_config = json.load(fp)

    model_dir = os.path.join(args.model_path, args.model)
    if not os.path.isdir(model_dir):
        raise FileNotFoundError(f"model path {model_dir} does not exist")

    if not os.path.isdir(args.static_path):
        raise FileNotFoundError(f"static content path {args.static_path} does not exist")

    # Initialize the model
    if 'LLaMA-2-7B-32K' in model_dir:
        model_class = Llama2TextGeneratorDriver
    elif 'RedPajama' in model_dir:
        model_class = RedPajamaTextGeneratorDriver
    else:
        model_class = PipelineTextGeneratorDriver

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
