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
