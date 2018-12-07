from django.core.management.base import BaseCommand
from gagp.models import Event
import datetime

class Command(BaseCommand):

    help = 'Expires event objects which are out-of-date'

    def handle(self, *args, **options):
        Event.objects.filter(date_of_event__lt=datetime.datetime.now()).delete()
