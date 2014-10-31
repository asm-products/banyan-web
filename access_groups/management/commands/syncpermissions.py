from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from access_groups.tasks import clean_stale_access
import pdb

class Command(BaseCommand):
    help = 'Syncs accesses to all the stories, and removes stale permissions.'
    
    def handle(self, *args, **options):
        clean_stale_access.delay()