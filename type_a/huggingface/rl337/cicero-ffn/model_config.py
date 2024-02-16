import transformers

from transformers import PretrainedConfig


class CiceroFFNConfig(PretrainedConfig):
    model_type = "CiceroFFN"
    input_width: int
    hidden_width: int
    hidden_depth: int
    output_width: int

    def __init__(self, 
                 input_width: int = 1,
                 hidden_width: int = 1, 
                 hidden_depth: int = 1,
                 output_width: int = 1, 
                 **kwargs):
        super().__init__(**kwargs)
        self.input_width = input_width
        self.hidden_width = hidden_width
        self.hidden_width = hidden_depth
        self.output_width = output_width
