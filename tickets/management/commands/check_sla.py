from django.core.management.base import BaseCommand
from tickets.models import Ticket

class Command(BaseCommand):
    help = 'Check all tickets for SLA status and send notifications.'

    def handle(self, *args, **kwargs):
        for ticket in Ticket.objects.all():
            ticket.check_and_notify_sla()
        self.stdout.write(self.style.SUCCESS('SLA checks and notifications complete.'))
