FROM python:3.9-slim

# Install dependencies
RUN pip install fastapi transformers torch

# Copy your script
COPY app.py /app/app.py

# Set work directory
WORKDIR /app

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]
