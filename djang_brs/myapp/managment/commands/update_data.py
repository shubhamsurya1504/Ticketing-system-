# your_app/management/commands/update_data.py
from django.core.management.base import BaseCommand
from myapp.models import Bus, User, Book, Registration
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Update data in the database'

    def handle(self, *args, **options):
        # Your update logic here
        # For example, set the status of all Book records to BOOKED every day
        Book.objects.all().update(status=Book.BOOKED)
        self.stdout.write(self.style.SUCCESS(f'Successfully updated data at {datetime.now()}'))
