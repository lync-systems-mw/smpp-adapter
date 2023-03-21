from django.core.management.base import BaseCommand, CommandError
from smpptransfer.utils.reader_helper import init_messages_fetch


class Command(BaseCommand):
    help = "Pulls unread messages from the SMC server"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Started pulling from [Airtel,TNM]"))
        init_messages_fetch()
