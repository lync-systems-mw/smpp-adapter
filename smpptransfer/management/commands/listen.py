from django.core.management.base import BaseCommand, CommandError
from smpptransfer.utils.reader_helper import init_messages_listen


class Command(BaseCommand):
    help = "Starts background threads to listen to SMSC events"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Started listening on [Airtel,TNM]"))
        init_messages_listen()
