from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from accounts.models import BanyanUser
import pdb

class Command(BaseCommand):
    args = '<username>'
    help = 'Sets the user with the given username as admin'
    
    option_list = BaseCommand.option_list + (
        make_option('--password',
            action='store',
            type='string',
            nargs=1,
            dest='password',
            default='admin',
            help='Password for the admin user'),
        )
    
    def handle(self, *args, **options):
        for username in args:
            try:
                user = BanyanUser.objects.get(username=username)
                '''
                Not using password for now because 'django.contrib.auth.backends.ModelBackend'
                Authorization Backend is not used
                '''
#                 user.set_password(options['password'])
                user.is_superuser = True
                user.is_staff = True
                user.save()
                self.stdout.write('"%s" is now an admin for the Banyan application' % username)
            except BanyanUser.DoesNotExist:
                raise CommandError('BanyanUser "%s" does not exist' % username)