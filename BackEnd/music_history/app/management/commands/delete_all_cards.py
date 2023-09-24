from django.core.management.base import BaseCommand
from ...models import Card

class Command(BaseCommand):
    help = 'Delete all cards from the database'

    def handle(self, *args, **kwargs):
        Card.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted all cards'))
