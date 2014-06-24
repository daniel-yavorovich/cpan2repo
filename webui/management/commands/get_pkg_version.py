from django.core.management.base import BaseCommand, CommandError
from webui.models import BuildConfiguration


class Command(BaseCommand):
    help = 'Get debian package version by build_conf id'

    def handle(self, *args, **options):
        self.stdout.write("{0}\n".format(BuildConfiguration.objects.get(pk=args[0]).version))