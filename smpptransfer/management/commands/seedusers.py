from django.contrib.auth.models import User
from django.contrib.auth.models import Permission

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create the default user accounts"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Started registering users."))

        credentials = [
            {"username": "admin0", "email": "admin0@app.com", "password": "@admin", "is_staff": True},
            {"username": "app", "email": "app@app.com", "password": "@app", "is_staff": False},
        ]

        for credential in credentials:
            try:
                user = User.objects.create_user(username=credential['username'],
                                                email=credential['email'],
                                                password=credential['password'],
                                                is_staff=credential['is_staff'], )

                # Add all permissions for the staff user
                if user.is_staff:
                    permissions = Permission.objects.all()

                    for permission in permissions:
                        user.user_permissions.add(permission)
            except:
                self.stdout.write(self.style.SUCCESS("Skipping user : {}".format(credential['username'])))

        self.stdout.write(self.style.SUCCESS("Finished seeding users."))
