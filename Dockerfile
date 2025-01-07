# Use the official Python 3.10 slim image
FROM python:3.10-slim

# Install system dependencies required for GDAL, PostgreSQL, and other dependencies
RUN apt-get update && \
    apt-get install -y \
    libgdal-dev \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Set Django settings module environment variable
ENV DJANGO_SETTINGS_MODULE=uksc_backend_django.settings
# Set GDAL library path for GeoDjango
ENV GDAL_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgdal.so

# Copy the current directory contents into the container
COPY . .

# Install the required Python packages from the requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port 8000 for the Django app
EXPOSE 8000

# Run the Django app on startup (or you can override this in docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
