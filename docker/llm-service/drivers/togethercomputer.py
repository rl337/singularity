import torch
from drivers.common import TextGeneratorRequest, TextGeneratorDriver
from transformers import AutoTokenizer, AutoModelForCausalLM, PreTrainedTokenizer, PreTrainedModel


# Driver for togethercomputer/Llama-2-7B-32K-Instruct
class Llama2TextGeneratorDriver(TextGeneratorDriver):
    tokenizer: PreTrainedTokenizer
    model: PreTrainedModel

    def initialize_generator(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path, local_files_only=True, trust_remote_code=True, torch_dtype=torch.float16)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)


    def generate_text(self, request: TextGeneratorRequest):
        input_ids = self.tokenizer.encode(request.prompt, return_tensors="pt")
        output = self.model.generate(input_ids, max_length=request.max_length, temperature=0.7, repetition_penalty=1.1, top_p=0.7, top_k=50)
        output_text = tokenizer.decode(output[0], skip_special_tokens=True)
        return {"generated_text": output_text}

# Driver for RedPajama-INCITE-Chat-3B-v1
class RedPajamaTextGeneratorDriver(TextGeneratorDriver):
    tokenizer: PreTrainedTokenizer
    model: PreTrainedModel

    def initialize_generator(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path, local_files_only=True, torch_dtype=torch.float16)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)


    def generate_text(self, request: TextGeneratorRequest):
        input_ids = self.tokenizer.encode(request.prompt, return_tensors="pt")

        inputs = self.tokenizer(request.prompt, return_tensors='pt').to(self.model.device)
        input_length = inputs.input_ids.shape[1]
        outputs = self.model.generate(
            **inputs, max_new_tokens=128, do_sample=True, temperature=0.7, top_p=0.7, top_k=50, return_dict_in_generate=True
        )
        token = outputs.sequences[0, input_length:]
        output_text = self.tokenizer.decode(token)
        return {"generated_text": output_text}
