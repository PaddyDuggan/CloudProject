# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of the src directory into /app directory inside the container
COPY src/ /app/

# Expose port 5000 to the outside world
EXPOSE 5000

# Install Flask and other dependencies
RUN pip install Flask flask-cors requests

# Set the command to run the Python script
CMD ["python", "functions.py"]


