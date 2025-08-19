# Use the official Python image as a parent image
FROM python:3.12-bullseye

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and model into the container
COPY . .

# Expose the port the app runs on (Cloud Run uses 8080 by default)
EXPOSE 8080

# Command to run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]