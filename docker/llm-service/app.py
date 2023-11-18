import argparse

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from transformers import pipeline



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


def create_generator(model_path):
    # Load the model from the specified path
    return pipeline('text-generation', model=model_path)

@app.get("/generate/")
def generate_text(prompt: str):
    result = generator(prompt, max_length=100)
    return {"generated_text": result[0]['generated_text']}

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    # Parse command line arguments for model path
    parser = argparse.ArgumentParser(description='LLM Service')
    parser.add_argument('model_path', type=str, help='Path to the model directory')
    args = parser.parse_args()

    # Initialize the model
    generator = create_generator(args.model_path)

    # Start the FastAPI app
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
