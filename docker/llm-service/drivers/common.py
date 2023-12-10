from typing import Optional
from transformers import pipeline, Pipeline


class TextGeneratorDriver:
    model_path: Optional[str] = None
    

    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path

    def initialize_generator(self):
        raise NotImplementedError("TextGeneratorDriver::initialize_generator must be implemented by subclasses")

    def generate_text(self, prompt: str):
        raise NotImplementedError("TextGeneratorDriver::generate_text must be implemented by subclasses")


class PipelineTextGeneratorDriver(TextGeneratorDriver):
    generator: Pipeline = None
    
    def initialize_generator(self):
        if self.generator is not None:
            return
        # Load the model from the specified path
        self.generator =  pipeline('text-generation', model=self.model_path)

    def generate_text(self, prompt: str):
        result = self.generator(prompt, max_length=1024)
        return {"generated_text": result[0]['generated_text'], "result": result}

