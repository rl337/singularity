import argparse
from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()

def create_generator(model_path):
    # Load the model from the specified path
    return pipeline('text-generation', model=model_path)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/generate/")
def generate_text(prompt: str):
    result = generator(prompt, max_length=100)
    return {"generated_text": result[0]['generated_text']}

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
