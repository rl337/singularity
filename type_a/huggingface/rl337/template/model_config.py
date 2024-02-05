import transformers

from transformers import PretrainedConfig
import json


class TemplateConfig(PretrainedConfig):
    model_type = "template"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
