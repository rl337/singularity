import unittest
import tempfile
import torch
from transformers import PreTrainedModel, PretrainedConfig

from singularity.models.basic.fnn import BaseFFNConfig, PreTrainedBaseFFN

class TestPreTrainedBaseFFN(unittest.TestCase):

    def set_model_to_known_state(self, model):
        # Manually set the model parameters to known values
        # Example: setting all weights of the first layer to 1
        with torch.no_grad():
            for p in model.parameters():
                p.fill_(1.0)

    def test_save_and_load(self):
        # Initialize the model
        config = BaseFFNConfig(input_size=100, hidden_size=50, output_size=10)
        model = PreTrainedBaseFFN(config)

        # Set the model to a known state
        self.set_model_to_known_state(model)

        # Save the model to a temporary directory
        with tempfile.TemporaryDirectory() as tmpdirname:
            model.save_pretrained(tmpdirname)

            # Load the model from the temporary directory
            loaded_model = PreTrainedBaseFFN.from_pretrained(tmpdirname)

            # Compare the loaded model to the original model
            for p_original, p_loaded in zip(model.parameters(), loaded_model.parameters()):
                self.assertTrue(torch.equal(p_original, p_loaded))

if __name__ == '__main__':
    unittest.main()

