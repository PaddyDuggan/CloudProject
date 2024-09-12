# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask and Requests via pip
RUN pip install Flask requests

# Expose port 93
EXPOSE 93

# Run proxy.py when the container launches
CMD ["python", "proxy.py"]
