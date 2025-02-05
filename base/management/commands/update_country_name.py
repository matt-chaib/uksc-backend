from django.core.management.base import BaseCommand
from base.models import CountryData

class Command(BaseCommand):
    help = "Update country name for United States of America to USA"

    def handle(self, *args, **kwargs):
        # Fetch the entry with the old name
        try:
            country = CountryData.objects.get(name="United States of America")
            country.name = "USA"  # Update the name
            country.save()  # Save changes to the database
            self.stdout.write(self.style.SUCCESS("Successfully updated country name to USA."))
        except CountryData.DoesNotExist:
            self.stdout.write(self.style.ERROR("Country 'United States of America' does not exist."))
