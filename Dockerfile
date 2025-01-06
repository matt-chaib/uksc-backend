# Use the official Python 3.10 slim image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Set Django settings module environment variable
ENV DJANGO_SETTINGS_MODULE=uksc_backend_django.settings

# Copy the current directory contents into the container
COPY . .

# Install the required Python packages from the requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port 8000 for the Django app
EXPOSE 8000
