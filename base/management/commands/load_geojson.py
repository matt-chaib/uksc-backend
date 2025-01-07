import json
from django.core.management.base import BaseCommand
from myapp.models import CountryData
from django.contrib.gis.geos import GEOSGeometry

class Command(BaseCommand):
    help = "Load GeoJSON data into the database"

    def handle(self, *args, **kwargs):
        with open('/path/to/countries.geojson') as f:
            geojson_data = json.load(f)
            for feature in geojson_data['features']:
                properties = feature['properties']
                geometry = GEOSGeometry(json.dumps(feature['geometry']))
                CountryData.objects.create(name=properties['name'], geom=geometry)