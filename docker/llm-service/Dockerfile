FROM nvidia/cuda:12.2.2-devel-ubuntu22.04

# Set the working directory in the container
WORKDIR /app

# Install Python and other necessary packages
RUN apt-get update && apt-get install -y python3-pip git

# Install PyTorch with CUDA 11.3 support
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

# Install the transformers and requests library
RUN pip3 install transformers requests sentencepiece ninja

# install flash-attn and this other thing in this sequence with these options
RUN pip install flash-attn --no-build-isolation
RUN pip install git+https://github.com/HazyResearch/flash-attention.git#subdirectory=csrc/rotary

RUN pip3 install fastapi uvicorn

# Copy your script and static files
COPY app.py /app/app.py
COPY static /app/static
COPY drivers /app/drivers

# Set work directory
WORKDIR /app

# Expose port
EXPOSE 8000

# Run the application
ENTRYPOINT ["python3", "app.py"]
