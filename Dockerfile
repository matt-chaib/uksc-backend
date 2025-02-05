# Use official Python slim image
FROM python:3.10-slim

# Install system dependencies required for GDAL, PostgreSQL, and other dependencies
RUN apt-get update && \
    apt-get install -y \
    libgdal-dev \
    gdal-bin \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean

# Set the working directory inside the container
WORKDIR /app

# Set environment variables
ENV DJANGO_SETTINGS_MODULE=uksc_backend_django.settings
ENV PYTHONUNBUFFERED=1
ENV GDAL_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgdal.so

# Copy the project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Collect static files
RUN python manage.py collectstatic --noinput

# Run database migrations
RUN python manage.py migrate --noinput

# Expose the port
EXPOSE 8000

# Run Gunicorn as the application server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "uksc_backend_django.wsgi:application"]
