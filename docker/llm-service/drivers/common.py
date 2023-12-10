from typing import Optional
from transformers import pipeline, Pipeline

from pydantic import BaseModel

class TextGeneratorRequest(BaseModel):
    prompt: str


class TextGeneratorDriver:
    model_path: Optional[str] = None
    

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path

    def initialize_generator(self):
        raise NotImplementedError("TextGeneratorDriver::initialize_generator must be implemented by subclasses")

    def generate_text(self, request: TextGeneratorRequest):
        raise NotImplementedError("TextGeneratorDriver::generate_text must be implemented by subclasses")

class PipelineTextGeneratorRequest(TextGeneratorRequest):
    max_length: int = 128
    pass


class PipelineTextGeneratorDriver(TextGeneratorDriver):
    generator: Pipeline = None
    
    def initialize_generator(self):
        if self.generator is not None:
            return
        # Load the model from the specified path
        self.generator =  pipeline('text-generation', model=self.model_path)

    def generate_text(self, request: PipelineTextGeneratorRequest):
        result = self.generator(request.prompt, max_length=request.max_length)
        return {"generated_text": result[0]['generated_text'], "result": result}

