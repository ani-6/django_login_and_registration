from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create groups structure'

    def handle(self, *args, **kwargs):
        try:
            new_group = Group(name="Users")
            new_group.save()
            new_group = Group(name="PlusUsers")
            new_group.save()
            new_group = Group(name="PUAdmin")
            new_group.save()
        except:
            print("Groups are already created!")