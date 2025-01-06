from django.db import models

# Create your models here.

class Supplier(models.Model):
    supplier = models.CharField(max_length=255)
    address = models.TextField()
    country = models.CharField(max_length=100)
    workers = models.IntegerField(null=True, blank=True)
    sector = models.CharField(max_length=100)
    year = models.IntegerField()
    source_business=models.CharField(max_length=100)

    def __str__(self):
        return self.supplier

class CountryCountView(models.Model):
    id = models.BigIntegerField(primary_key=True)
    source_business = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    year = models.IntegerField()
    country_count = models.IntegerField()

    class Meta:
        managed = False  # This prevents Django from trying to manage the table
        db_table = 'country_count_by_year_and_supermarket'