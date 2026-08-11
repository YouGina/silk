from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from demo.models import Note


class Command(BaseCommand):
    def handle(self, *a, **k):
        Note.objects.get_or_create(title="victim-private-record", body="top secret")
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "a@e.com", "adminpass")
