from django.contrib.auth.models import User, Group
from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from ...models import *

class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')
        parser.add_argument('-p', '--prefix', type=str, help='Define a username prefix')
        parser.add_argument('-a', '--admin', action='store_true', help='Create an admin account')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        prefix = kwargs['prefix']
        admin = kwargs['admin']
        password='test@123'
        adminpassword = 'serveradmin987'

        for i in range(total):
            if prefix:
                username = '{prefix}_{random_string}'.format(prefix=prefix, random_string=get_random_string(6))
            else:
                username = get_random_string(8)

            if admin:
                try:
                    user = User.objects.create_superuser(username='admin',first_name='Admin', email='admin@localhost.com', password=adminpassword)
                    Home_LatestUpdates.objects.create(user=user,update='Welcome to the Hub!')
                    try:
                        obj = Home_ImportantLinks.objects.create(heading='Maintenance mode ON',description='Turn ON maintenance mode',link='maintenance-mode/on',is_active=True)
                        obj.user.add(user)
                        obj.save()
                        obj2 = Home_ImportantLinks.objects.create(heading='Maintenance mode OFF',description='Turn OFF maintenance mode',link='maintenance-mode/off',is_active=True)
                        obj2.user.add(user)
                        obj2.save()
                    except:
                        print("Unable to add Maintenancemode links")
                    self.stdout.write('AdminUser "%s (%s)" created successfully with password-"%s"!' % (user.username, user.id,adminpassword))
                except:
                    print("Admin user is already created.")
            else:
                user = User.objects.create_user(username=username,first_name=username, email='', password=password)
                my_group = Group.objects.get(name='Users') 
                user.groups.add(my_group)
                self.stdout.write('User "%s (%s)" created successfully with password "%s"!' % (user.username, user.id, password))