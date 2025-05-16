# Use the official Python slim image to keep the image size small
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application code into the container
COPY . .

# Install system dependencies (for subprocess and docker)
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir flask python-docker

# Expose the port the app runs on
EXPOSE 5802

# Command to run the Flask app
CMD ["python", "app.py"]