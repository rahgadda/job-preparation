# Use the official Python image as a base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies needed by your application
RUN pip install --no-cache-dir langchain-google-genai google.generativeai python-dotenv langchain langchain_community Flask

# Expose the port the Flask app runs on
EXPOSE 7860

# Define the command to run your application
CMD ["python", "google-genai-local-server.py"]