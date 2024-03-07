from transformers import PreTrainedModel
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
from .model_config import CiceroFFNConfig

class CiceroFFN(nn.Module):
    input_layer: nn.Linear
    hidden_layers: nn.ModuleList
    output_layer: nn.Linear

    def __init__(self, 
                 input_width: int, 
                 hidden_width: int, 
                 hidden_depth: int, 
                 output_width: int):
        super().__init__()

        self.input_layer = nn.Linear(input_width, hidden_width)

        self.hidden_layers = nn.ModuleList()
        for _ in range(hidden_depth):
            self.hidden_layers.append(nn.Linear(hidden_width, hidden_width))

        self.output_layer = nn.Linear(hidden_width, output_width)

    def forward(self, input: Tensor) -> Tensor:
        this_pass = F.relu(self.input_layer(input))
        for layer in self.hidden_layers:
            this_pass = F.relu(layer(this_pass))
        output = self.output_layer(this_pass)
        return output[:, -1, :]

class CiceroFFNModel(PreTrainedModel):
    config_class = CiceroFFNConfig
    model: CiceroFFN

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = CiceroFFN(
            input_width=config.input_width,
            hidden_width=config.hidden_width,
            hidden_depth=config.hidden_depth,
            output_width=config.output_width
        )

    def forward(self, input_ids, **kwargs):
        return self.model(input_ids, **kwargs)
