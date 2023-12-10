import argparse
import os.path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from drivers import PipelineTextGeneratorDriver


def create_generator(model_path):
    # Load the model from the specified path
    return pipeline('text-generation', model=model_path)

if __name__ == "__main__":
    # Parse command line arguments for model path
    parser = argparse.ArgumentParser(description='LLM Service')
    parser.add_argument('model_path', type=str, help='Path to the model directory')
    parser.add_argument('model', type=str, help='the name and commit hash of the model')
    args = parser.parse_args()

    model_dir = os.path.join(args.model_path, args.model)
    if not os.path.isdir(model_dir):
        raise FileNotFoundError(f"model path {model_dir} does not exist")

    # Initialize the model
    model = PipelineTextGeneratorDriver(model_dir)
    model.initialize_generator()

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )

    app.add_api_route(path="/generate/", endpoint=model.generate_text, methods=["GET"])
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
    
    # Start the FastAPI app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
