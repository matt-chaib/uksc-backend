from rest_framework import serializers
from .models import Supplier
from .models import CountryCountView

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'supplier', 'address', 'country', 'workers', 'sector', 'year', 'source_business']

class CountryCountViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryCountView
        fields = ['id', 'year', 'source_business', 'country', 'count']