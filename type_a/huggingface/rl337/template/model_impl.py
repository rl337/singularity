from transformers import PreTrainedModel
import torch.nn as nn
import torch.nn.functional as F
from .model_config import TemplateConfig

class TrivialFNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.hidden = nn.Linear(1, 1)

    def forward(self, x):
        w = F.relu(self.hidden(x))
        return self.output(w)

class TemplateModel(PreTrainedModel):
    config_class = TemplateConfig
    model: TrivialFNN

    def __init__(self, config, **kwargs):
        super().__init__(config, **kwargs)
        self.model = TrivialFNN()

    def forward(self, input_ids, **kwargs):
        return self.model(input_ids, **kwargs)
