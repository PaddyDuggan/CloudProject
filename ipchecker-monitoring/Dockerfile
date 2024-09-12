# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl

# Copy the current directory contents into the container at /app
COPY . /app

# Run periodic_test.py script
CMD ["python", "periodic_test.py"]
