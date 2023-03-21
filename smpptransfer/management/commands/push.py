from django.core.management.base import BaseCommand, CommandError
from smpptransfer.utils.sender_helper import init_sending_scheduled_messages


class Command(BaseCommand):
    help = "Pushes unsent messages to the SMC server"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Started sending..."))
        init_sending_scheduled_messages()
