import argparse
import logging
import os.path
import json
import importlib

from typing import Optional, Dict, List, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from drivers.common import TextGeneratorDriver, TextGeneratorRequest

from pydantic import BaseModel

class ModelConfigRequest(BaseModel):
    name: Optional[str] = None

class RequestHandler:
    
    def initialize_handler(self):
        raise NotImplementedError("RequestHandler::initialize_handler must be implemented by subclasses")

    def get_handle_method(self) -> Any:
        raise NotImplementedError("RequestHandler::handle must be implemented by subclasses")

    def path(self) -> str:
        raise NotImplementedError("RequestHandler::path must be implemented by subclasses")

    def methods(self) -> List[str]:
        return ["POST"]

class ModelConfigHandler(RequestHandler):
    active_model_name: str
    model_list_config: Dict[str, Any]

    def __init__(self,  model_name: str, model_list_config: Dict[str, Dict[str, Any]]):
        self.active_model_name = model_name
        self.model_list_config = model_list_config

    def initialize_handler(self):
        model_name = self.active_model_name
        model_list = list(self.model_list_config.keys())
        if model_name not in model_list:
            raise ValueError(f"model {model_name} must be one of {model_list}")

    def handle(self, request: ModelConfigRequest):
        model_name = request.name
        if model_name is None:
            model_name = self.active_model_name
        model_list = list(self.model_list_config.keys())
        if model_name not in model_list:
            raise ValueError(f"model {model_name} must be one of {model_list}")
        return { "model": model_name, "config": self.model_list_config[model_name] }

    def get_handle_method(self):
        return self.handle

    def path(self):
        return '/model_config/'

    def methods(self) -> List[str]:
        return ["GET", "POST"]

class GenerateTextHandler(RequestHandler):
    model_name: str
    model_config: Dict[str, Any]
    model: Optional[TextGeneratorDriver]

    def __init__(self,  model_name: str, model_config: Dict[str, Any]):
        self.model_name = model_name
        self.model_config = model_config
        self.model = None

    def initialize_handler(self):
        if "driver" not in model_config:
            raise ValueError(f"model {args.model} from {args.model_list_config} not configured with driver.")
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
        self.model = model_class(model_dir)
        self.model.initialize_generator()

    def get_handle_method(self):
        return self.model.generate_text

    

    def path(self):
        return '/generate/'


def load_model_list_config(filename: str) -> Dict[str, Any]:

    with open(args.model_list_config, 'r') as fp:
        model_list_config = json.load(fp)

        default_config = {"args": {}}
        if "default" in model_list_config:
            default_config = model_list_config["default"]
        model_list_config.pop("default", None)

        result = {}
        for model_name in model_list_config:
            result[model_name] = { **default_config, **model_list_config[model_name] }
            result[model_name]["args"] = { **default_config["args"], **model_list_config[model_name]["args"] }
    
        return result

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Parse command line arguments for model path
    parser = argparse.ArgumentParser(description='LLM Service')
    parser.add_argument('model_list_config', type=str, help='Path to the model config json')
    parser.add_argument('model_path', type=str, help='Path to the model directory')
    parser.add_argument('static_path', type=str, help='Path to static files for webapp')
    parser.add_argument('model', type=str, help='the name and commit hash of the model')
    args = parser.parse_args()

    # validate static content directory
    if not os.path.isdir(args.static_path):
        raise FileNotFoundError(f"static content path {args.static_path} does not exist")

    # validate that path to models.json exists
    if not os.path.isfile(args.model_list_config):
        raise FileNotFoundError(f"config path {args.model_list_config} does not exist")

    model_list_config = load_model_list_config(args.model_list_config)
    logging.info(f"using model configs: {json.dumps(model_list_config, indent=2)}")

    models_list = list(model_list_config.keys())
    if args.model not in models_list:
        raise ValueError(f"model {args.model} was not found in {models_list}")

    model_config = model_list_config[args.model]

    handlers = [
        GenerateTextHandler(args.model, model_config),
        ModelConfigHandler(args.model, model_list_config),
    ]

    for handler in handlers:
        handler.initialize_handler()

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    for handler in handlers:
        handler_path = handler.path()
        logging.info(f"adding api route {handler_path} to {handler.__class__.__name__}")
        app.add_api_route(path=handler_path, endpoint=handler.get_handle_method(), methods=handler.methods())
    app.mount("/", StaticFiles(directory=args.static_path, html=True), name="static")
    
    # Start the FastAPI app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
