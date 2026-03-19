# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy all your files into the container
COPY . /app

# Install the required libraries
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Hugging Face port
EXPOSE 7860

# Command to run the app
CMD ["python", "app.py"]
