from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Supplier
from .models import CountryCountView
from .models import CountryData
import json

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'supplier', 'address', 'country', 'workers', 'sector', 'year', 'source_business']

class CountryCountViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryCountView
        fields = ['id', 'year', 'source_business', 'country', 'count']

class CountryDataSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = CountryData
        fields = ('id', 'name')  # You can add any other fields you'd like to include
        geo_field = 'geom'

    # def to_representation(self, instance):
    #     """
    #     Ensure that the geometry is serialized as a proper GeoJSON object
    #     rather than a raw string (e.g., "SRID=4326;POLYGON(...))").
    #     """
    #     representation = super().to_representation(instance)
    #     # Explicitly serialize the geometry as GeoJSON
    #     # Ensure that geojson is not serialized as a string but as an actual GeoJSON object
    #     representation['geometry'] = instance.geom.geojson
    #     return representation