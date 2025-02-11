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

COPY data/total_data.csv /app/data/total_data.csv
COPY data/countries.geo.json /app/data/countries.geo.json

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && pip install -r requirements.txt

# Expose the port
EXPOSE 8000

# Run entrypoint script
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]