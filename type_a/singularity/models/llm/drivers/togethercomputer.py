import torch
import logging
import sys

from drivers.common import TextGeneratorRequest, TextGeneratorDriver
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoConfig, PreTrainedTokenizer, PreTrainedModel, PretrainedConfig
from torch.quantization import quantize_dynamic



class Llama2TextGeneratorRequest(TextGeneratorRequest):
    max_new_tokens: int
    do_sample: bool
    temperature: float
    top_p: float
    top_k: int

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


class RedPajamaTextGeneratorRequest(TextGeneratorRequest):
    max_new_tokens: int
    do_sample: bool
    temperature: float
    top_p: float
    top_k: int
    return_dict_in_generate: bool

# Driver for RedPajama-INCITE-Chat-3B-v1
class RedPajamaTextGeneratorDriver(TextGeneratorDriver):
    tokenizer: PreTrainedTokenizer
    model: PreTrainedModel

    def initialize_generator(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_path, local_files_only=True, torch_dtype=torch.float16)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(device)

    def generate_text(self, request: RedPajamaTextGeneratorRequest):
        input_ids = self.tokenizer.encode(request.prompt, return_tensors="pt")

        kwargs = request.dict()
        kwargs.pop("prompt", None)
        logging.info(f"request was: {kwargs}")

        inputs = self.tokenizer(request.prompt, return_tensors='pt').to(self.model.device)
        input_length = inputs.input_ids.shape[1]
        outputs = self.model.generate(**kwargs, **inputs)
        # outputs = self.model.generate(
        #     **inputs, max_new_tokens=128, do_sample=True, temperature=0.7, top_p=0.7, top_k=50, return_dict_in_generate=True
        # )
        token = outputs.sequences[0, input_length:]
        output_text = self.tokenizer.decode(token)
        return {"generated_text": output_text}


class StripedHyenaTextGeneratorRequest(TextGeneratorRequest):
    max_new_tokens: int
    temperature: float
    top_p: float
    top_k: int
    repetition_penalty: float
    penalty_alpha: float
    do_sample: bool
    eos_token_id: int 

# Driver for StripedHyena-Nous-7B 
class StripedHyenaTextGeneratorDriver(TextGeneratorDriver):
    tokenizer: PreTrainedTokenizer
    model: PreTrainedModel
    config: PretrainedConfig

    def initialize_generator(self):
        logging.info(f"initializing from {self.model_path}")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            model_max_length=sys.maxsize,
            trust_remote_code=True,
            local_files_only=True
        )
        self.config = AutoConfig.from_pretrained(
            self.model_path,
            trust_remote_code=True,
            local_files_only=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            trust_remote_code=True,
            config=self.config,
            local_files_only=True
        )

        # device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        device = "cpu"
        self.model.to(device)

    def generate_text(self, request: StripedHyenaTextGeneratorRequest):
        input_ids = self.tokenizer.encode(request.prompt, return_tensors="pt")

        kwargs = request.dict()
        kwargs.pop("prompt", None)
        logging.info(f"request was: {kwargs}")

        inputs = self.tokenizer(request.prompt, return_tensors='pt').to(self.model.device)
        input_length = inputs.input_ids.shape[1]
        outputs = self.model.generate(**kwargs, **inputs)
        token = outputs.sequences[0, input_length:]
        output_text = self.tokenizer.decode(token)
        return {"generated_text": output_text}
