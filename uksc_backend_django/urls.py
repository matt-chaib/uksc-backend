"""
URL configuration for uksc_backend_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from base.views import *
from base.views import CountryDataGeoJsonView

router = DefaultRouter()
router.register(r'base', SupplierViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('all', get_all, name="get_all"), 
    path('health/', health_check, name='health_check'),
    path('suppliers-head/', get_supplier_data, name='get_supplier_data'),
    path('country-count-business/<int:year>/', count_country_by_year_and_supermarket, name='country-count-by-year-and-supermarket'),
    path('country-count/<int:year>/', count_country_by_year, name='country-count-by-year'),
    path('api/countries/', CountryDataGeoJsonView.as_view(), name='country-data'),
    path('business-count/<int:year>/', count_supermarket_by_year_and_country, name='business-count')
]
