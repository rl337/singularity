from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()

# Initialize the model
generator = pipeline('text-generation', model='gpt2')

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/generate/")
def generate_text(prompt: str):
    result = generator(prompt, max_length=100)
    return {"generated_text": result[0]['generated_text']}
