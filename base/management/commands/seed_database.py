import pandas as pd
from django.core.management.base import BaseCommand
import django
import os

django.setup()

from base.models import Supplier

class Command(BaseCommand):
    help = 'Seeds the database with data from a pandas DataFrame'

    def handle(self, *args, **kwargs):
        # Determine the correct path dynamically
        docker_path = '/app/data/total_data.csv'  # Path inside Docker container
        local_path = 'data/total_data.csv'  # Path in local development

        # Check which path exists
        if os.path.exists(docker_path):
            file_path = docker_path  # Running inside Docker
        elif os.path.exists(local_path):
            file_path = local_path  # Running in local development
        else:
            raise FileNotFoundError("total_data.csv not found in either /app/data/ or ./data/")


        df = pd.read_csv(file_path)  # or use any method to load your DataFrame
        print(df)
        workers = 0 # row['workers'] if pd.notna(row['workers']) else 0 # Set to None if NaN


        # Iterate through the rows of the DataFrame and create model instances
        for _, row in df.iterrows():
            # Create and save a FoodSupplier object from the DataFrame row
            Supplier.objects.create(
                supplier=row['supplier'],
                address=row['address'],
                country=row['country'],
                workers=workers,
                sector=row['sector'],
                year=row['year'],
                source_business=row['source_business']
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded the database with supplier data'))
