FROM 0-singularity-base

ARG PROJECT_DIR
ARG CONFIG_DIR

# Set the working directory in the container
WORKDIR /app

# Install Python and other necessary packages
RUN apt-get update && apt-get install -y python3-pip

# Install PyTorch with CUDA 11.3 support
RUN pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113

# Install the transformers and requests library
RUN pip3 install transformers requests

# Copy the Python script into the container at /app
COPY ${PROJECT_DIR}/app.py /app/app.py
COPY ${CONFIG_DIR} /app/config


# Define the entrypoint
ENTRYPOINT ["python3", "app.py"]

