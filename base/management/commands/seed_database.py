import pandas as pd
from django.core.management.base import BaseCommand
import django

django.setup()

from base.models import Supplier

class Command(BaseCommand):
    help = 'Seeds the database with data from a pandas DataFrame'

    def handle(self, *args, **kwargs):
        # Load your pandas DataFrame from your script
        # Example: Assuming your pandas script is inside /scripts and creates a DataFrame
        df = pd.read_csv('output_data/total_data.csv')  # or use any method to load your DataFrame
        print(df)
        workers = 0 # row['workers'] if pd.notna(row['workers']) else 0 # Set to None if NaN

        country_dictionary = {
        "Türkiye": "Turkey",
        "Cyprus (South)": "Cyprus",
        """Republic of                     +
        | Ireland""": "Ireland",
        "United States": "USA",
        "Scotland": "United Kingdom"
    }

        df['country'] = df['country'].apply(lambda x: country_dictionary.get(x, x))


        # Iterate through the rows of the DataFrame and create model instances
        for _, row in df.iterrows():
        #     if "KATSOU" in row['supplier']:
        #         print(row)
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
