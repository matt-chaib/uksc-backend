from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Supplier
from .serializers import SupplierSerializer
from django.http import JsonResponse

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


def health_check(request):
    return JsonResponse({"status": "running"})

def get_supplier_data(request):
    # Query the first 10 suppliers
    suppliers = Supplier.objects.all()[:10]

    # Convert the queryset to a list of dictionaries
    suppliers_list = list(suppliers.values())

    # Return the data as JSON
    return JsonResponse(suppliers_list, safe=False)