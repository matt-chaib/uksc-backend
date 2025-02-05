from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Supplier
from .serializers import SupplierSerializer
from django.http import JsonResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from .models import CountryData
from .serializers import CountryDataSerializer
from django.core.serializers import serialize
from rest_framework.views import APIView
import json
from collections import defaultdict
from django.db.models import Q

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


def health_check(request):
    return JsonResponse({"status": "running"})

def get_all(request):
    # Query the first 10 suppliers
    suppliers = Supplier.objects.all()

    # Convert the queryset to a list of dictionaries
    suppliers_list = list(suppliers.values())

    # Return the data as JSON
    return JsonResponse(suppliers_list, safe=False)

def get_supplier_data(request):
    # Query the first 10 suppliers
    suppliers = Supplier.objects.all()[:10]

    # Convert the queryset to a list of dictionaries
    suppliers_list = list(suppliers.values())

    # Return the data as JSON
    return JsonResponse(suppliers_list, safe=False)

@api_view(['GET'])
def count_country_by_year_and_supermarket(request, year):
    data = (
        Supplier.objects.filter(year=year)
        .values('source_business', 'country')
        .annotate(country_count=Count('country'))
        .order_by('source_business', 'country')
    )

    all_countries = {entry["country"] for entry in data}

    result_dict = defaultdict(dict)

    for entry in data:
        country = entry["country"]
        business = entry["source_business"]
        count = entry["country_count"]
        result_dict[business]["source_business"] = business  # Ensure country is always set
        result_dict[business][country] = count     # Set business count for each source_business

    for business_data in result_dict.values():
        for country in all_countries:
            business_data.setdefault(country, 0)
    # Convert the grouped data into a list
    result = list(result_dict.values())


    # Return the results as JSON
    return Response(result)

@api_view(['GET'])
def count_supermarket_by_year_and_country(request, year):

    asda_sectors = [
        'Agriculture', 'Food Manufacturing', 'Pharmaceuticals', 'Crop Production',
        'Food Industry', 'Food & Beverage', 'Food', 'Chemicals', 'Beverages',
        'Animal Production', 'Farming'
    ]

    data = (
        Supplier.objects.filter(year=year)
        # .filter(
        #     Q(source_business='Asda', sector__in=asda_sectors) | ~Q(source_business='Asda')
        # )
        .values('source_business', 'country')
        .annotate(business_count=Count('source_business'))
        .order_by('source_business', 'country')
    )

    all_businesses = {entry["source_business"] for entry in data}

    result_dict = defaultdict(dict)

    for entry in data:
        country = entry["country"]
        business = entry["source_business"]
        count = entry["business_count"]
        result_dict[country]["country"] = country  # Ensure country is always set
        result_dict[country][business] = count     # Set business count for each source_business

    for country_data in result_dict.values():
        for business in all_businesses:
            country_data.setdefault(business, 0)
    # Convert the grouped data into a list
    result = list(result_dict.values())

    # Return the results as JSON
    return Response(result)

@api_view(['GET'])
def count_country_by_year(request, year):
    source_business = request.GET.get('source_business')  # Retrieve the source_business from query parameters

    # Base queryset
    queryset = Supplier.objects.filter(year=year)

    if source_business:  # Apply filter if source_business is provided
        queryset = queryset.filter(source_business=source_business)

    result = (
        queryset
        .values('country')
        .annotate(count=Count('country'))
        .order_by('country')
    )

    # Return the results as JSON
    return Response(result)

class CountryDataGeoJsonView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        geojson_data = serialize(
            "geojson", 
            CountryData.objects.all(), 
            geometry_field="geom", 
            fields=("name",)
        )
        geojson_object = json.loads(geojson_data)  # Convert to dict
        features_list = geojson_object["features"]  # Extract features only
        return JsonResponse(features_list, safe=False)  # Send features as JSON