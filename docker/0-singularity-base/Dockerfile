ARG PROJECT_DIR
ARG CONFIG_DIR

FROM nvidia/cuda:12.2.2-devel-ubuntu22.04

# Install Python and other necessary packages
RUN apt-get update && apt-get install -y python3-pip git
RUN pip install --no-cache-dir --upgrade pip

# Install PyTorch with CUDA 11.3 support
# RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113
RUN pip3 install torch torchvision torchaudio 

# Install requirements that don't need special instruction
RUN pip3 install transformers requests sentencepiece ninja argparse bz2file mwparserfromhell pytest tokenizers mock

# install flash-attn and this other thing in this sequence with these options
#RUN pip install flash-attn --no-build-isolation
#RUN pip install git+https://github.com/HazyResearch/flash-attention.git#subdirectory=csrc/layer_norm
#RUN pip install git+https://github.com/HazyResearch/flash-attention.git#subdirectory=csrc/rotary

RUN apt-get install -y vim
