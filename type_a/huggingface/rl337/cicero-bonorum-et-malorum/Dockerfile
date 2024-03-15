# Use an official Ubuntu base image
FROM ubuntu:latest

# Set the working directory in the container
WORKDIR /usr/src/app

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Copy the requirements.txt file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of your project's source code from your host to your image filesystem.
COPY . /cicero-bonorum-et-malorum

# Run test_dataset.py when the container launches
CMD ["python3", "/cicero-bonorum-et-malorum/test_dataset.py"]
