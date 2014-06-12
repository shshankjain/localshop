"""
Management utility to create secret keys.
"""
import uuid
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from localshop.apps.permissions.models import Credential

class Command(BaseCommand):
    """
    """

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.UserModel = get_user_model()

    option_list = BaseCommand.option_list
    help = 'Used to create a secret keys.'

    def handle(self, *args, **options):
        superuser = self.UserModel.objects.filter(is_staff=True, is_active=True, is_superuser=True)
        if not superuser:
            raise CommandError("You must create a superuser before creating secret keys.")
        superuser = superuser[0]

        Credential.objects.create(
            access_key = uuid.UUID('{%s}'%getattr(settings, 'CREDENTIAL_ACCESS_KEY', '00010203-0405-0607-0809-0a0b02340e0f')),
            creator = superuser,
            secret_key = uuid.UUID('{%s}'%getattr(settings, 'CREDENTIAL_SECRET_KEY', '00010203-0405-0607-0809-0a0b02340e0f'))
        )
