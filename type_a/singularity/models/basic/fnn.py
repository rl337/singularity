import torch
import torch.nn as nn
import torch.nn.functional as F

from transformers import PreTrainedModel, PretrainedConfig

class BaseFFN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(BaseFFN, self).__init__()
        # First hidden layer
        self.hidden1 = nn.Linear(input_size, hidden_size)
        # Second hidden layer
        self.hidden2 = nn.Linear(hidden_size, hidden_size)
        # Output layer
        self.output = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        # Pass the input through the first hidden layer, then apply ReLU
        x = F.relu(self.hidden1(x))
        # Pass through the second hidden layer, then apply ReLU
        x = F.relu(self.hidden2(x))
        # Pass through the output layer
        x = self.output(x)
        return x


class BaseFFNConfig(PretrainedConfig):
    model_type = "base_ffn"
    input_size: int
    hidden_size: int
    output_size: int


class PreTrainedBaseFFN(PreTrainedModel):
    config_class = BaseFFNConfig
    ffn_model: BaseFFN

    def __init__(self, config):
        super().__init__(config)
        self.simple_ffn = BaseFFN(config.input_size, config.hidden_size, config.output_size)

    def forward(self, input_ids, **kwargs):
        return self.simple_ffn(input_ids)

