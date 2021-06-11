from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from core.models import AVGRegisterline


def excelboolean(excelvalue):
    return excelvalue in ['Ja', 'ja']

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    @transaction.atomic
    def handle(self, *args, **options):
        print("Doing it")
        AVGRegisterline.objects.all().delete()