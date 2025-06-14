from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone


class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    sla_missed = models.BooleanField(default=False)
    sla_warning_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def check_and_notify_sla(self):
        if not self.sla_missed and timezone.now() > self.deadline:
            self.sla_missed = True
            self.save()
            send_mail(
                subject=f"SLA Missed: {self.title}",
                message=f"Ticket '{self.title}' has missed its SLA deadline.",
                from_email=None,
                recipient_list=[self.owner.email],
                fail_silently=True,
            )
        elif (
            not self.sla_warning_sent
            and (self.deadline - timezone.now()).total_seconds() < 3600
            and timezone.now() < self.deadline
        ):
            self.sla_warning_sent = True
            self.save()
            send_mail(
                subject=f"SLA Warning: {self.title}",
                message=f"Ticket '{self.title}' is about to miss its SLA deadline in less than 1 hour.",
                from_email=None,
                recipient_list=[self.owner.email],
                fail_silently=True,
            )
