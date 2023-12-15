import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedTokenizer, PreTrainedModel


# Driver for togethercomputer/Llama-2-7B-32K-Instruct
class Llama2TextGeneratorDriver:
    tokenizer: PreTrainedTokenizer
    model: PreTrainedModel

    def initialize_generator(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path, local_files_only=True, trust_remote_code=True, torch_dtype=torch.float16)

    def generate_text(self, request: TextGeneratorRequest):
        input_ids = self.tokenizer.encode(request.prompt, return_tensors="pt")
        output = self.model.generate(input_ids, max_length=request.max_length, temperature=0.7, repetition_penalty=1.1, top_p=0.7, top_k=50)
        output_text = tokenizer.decode(output[0], skip_special_tokens=True)
        return {"generated_text": output_text}

