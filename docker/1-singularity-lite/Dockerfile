FROM ubuntu:22.04

# Install Python and other necessary packages
RUN apt-get update && apt-get install -y python3-pip git
RUN pip install --no-cache-dir --upgrade pip

# Install PyTorch with CUDA 11.3 support
RUN pip3 install torch torchvision torchaudio 

# Install requirements that don't need special instruction
RUN pip3 install transformers requests pytest tokenizers mock

RUN apt-get install -y vim
