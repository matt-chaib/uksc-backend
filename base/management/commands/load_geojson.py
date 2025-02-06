import json
from django.core.management.base import BaseCommand
from base.models import CountryData
from django.contrib.gis.geos import GEOSGeometry
import os

class Command(BaseCommand):
    help = "Load GeoJSON data into the database"

    def handle(self, *args, **kwargs):
        # Determine the correct path dynamically
        docker_path = '/app/data/countries.geo.json'  # Path inside Docker container
        local_path = 'data/countries.geo.json'  # Path in local development

        # Check which path exists
        if os.path.exists(docker_path):
            file_path = docker_path  # Running inside Docker
        elif os.path.exists(local_path):
            file_path = local_path  # Running in local development
        else:
            raise FileNotFoundError("countries.geo.json not found in either /app/data/ or ./data/")


        with open(file_path) as f:
            geojson_data = json.load(f)
            for feature in geojson_data['features']:
                properties = feature['properties']
                if properties['name'] == "United States of America":
                    properties['name'] = "USA"
                geometry = GEOSGeometry(json.dumps(feature['geometry']))
                CountryData.objects.create(name=properties['name'], geom=geometry)
