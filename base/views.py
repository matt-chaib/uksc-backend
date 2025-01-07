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
    result = (
        Supplier.objects.filter(year=year)
        .values('source_business', 'country')
        .annotate(country_count=Count('country'))
        .order_by('source_business', 'country')
    )

    # Return the results as JSON
    return Response(result)

@api_view(['GET'])
def count_country_by_year(request, year):
    result = (
        Supplier.objects.filter(year=year)
        .values('country')
        .annotate(count=Count('country'))
        .order_by('country')
    )

    # For debugging: print results to the console
    for item in result:
        print(item)

    # Return the results as JSON
    return Response(result)

class CountryDataGeoJsonView(APIView):
    def get(self, request, *args, **kwargs):
        # Serialize the queryset to GeoJSON, ensuring it's returned as a proper object
        geojson_data = serialize(
            "geojson", 
            CountryData.objects.all(), 
            geometry_field="geom",  # Specify the geometry field
            fields=["id", "name"]   # Specify other fields to include
        )
        geojson_square = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [0, 0],  # Bottom-left corner
                        [1, 0],  # Bottom-right corner
                        [1, 1],  # Top-right corner
                        [0, 1],  # Top-left corner
                        [0, 0]   # Close the polygon back to the starting point
                    ]
                ]
            },
            "properties": {
                "name": "Simple Square"
            }
        }
    ]
}

        # Ensure geojson_data is a valid Python dictionary, not a string
        return JsonResponse(geojson_square, safe=False)
