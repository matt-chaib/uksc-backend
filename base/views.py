from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Supplier
from .serializers import SupplierSerializer
from django.http import JsonResponse
from django.db.models import Count
from rest_framework.decorators import api_view
from rest_framework.response import Response

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

    # For debugging: print results to the console
    for item in result:
        print(f"Supermarket: {item['source_business']}, Country: {item['country']}, Count: {item['country_count']}")

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