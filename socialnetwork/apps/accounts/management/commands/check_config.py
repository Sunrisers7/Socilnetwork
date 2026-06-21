from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Check Django configuration'

    def handle(self, *args, **options):
        self.stdout.write(f"DEBUG: {settings.DEBUG}")
        self.stdout.write(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")
        self.stdout.write(f"SECRET_KEY: {'Set' if settings.SECRET_KEY else 'NOT SET!'}")
        self.stdout.write(f"DATABASES: {settings.DATABASES['default']['ENGINE']}")

        if not settings.DEBUG and not settings.ALLOWED_HOSTS:
            self.stdout.write(self.style.ERROR(
                'ERROR: ALLOWED_HOSTS is empty and DEBUG is False!'
            ))
        else:
            self.stdout.write(self.style.SUCCESS('Configuration looks good!'))