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
            # Save before attempting to send email
            try:
                print(f"[DEBUG] Preparing to send SLA Missed email for ticket '{self.title}' to {self.owner.email}")
                send_mail(
                    subject=f"SLA Missed: {self.title}",
                    message=f"Ticket '{self.title}' has missed its SLA deadline.",
                    from_email=None, # Uses DEFAULT_FROM_EMAIL from settings
                    recipient_list=[self.owner.email],
                    fail_silently=False, # Changed in previous step
                )
                print(f"[EMAIL SUCCESS] SLA Missed email sent for ticket '{self.title}' to {self.owner.email}")
                self.save() # Save after successful email send
            except Exception as e:
                print(f"[EMAIL ERROR] Failed to send SLA Missed email for ticket '{self.title}' to {self.owner.email}. Error: {e}")
                # Optionally, re-raise the exception if you want the command to fail loudly
                # or handle the fact that the ticket was marked sla_missed but email failed.
                # For now, just log and the sla_missed status is already set.
                # self.save() might be called here if partial state should be saved despite email failure.
                # Current logic: sla_missed is True, email fails, ticket reflects sla_missed but no email sent.
                # Re-saving self.sla_missed = True here is redundant if it was already True.
                # If email must succeed for sla_missed to be true, then move self.sla_missed = True inside try.
                # For now, we assume setting sla_missed is independent of email success.
                # We will save the sla_missed status regardless of email outcome for now.
                self.save()
        elif (
            not self.sla_warning_sent
            and (self.deadline - timezone.now()).total_seconds() < 3600
            and timezone.now() < self.deadline
        ):
            self.sla_warning_sent = True
            # Save before attempting to send email
            try:
                print(f"[DEBUG] Preparing to send SLA Warning email for ticket '{self.title}' to {self.owner.email}")
                send_mail(
                    subject=f"SLA Warning: {self.title}",
                    message=f"Ticket '{self.title}' is about to miss its SLA deadline in less than 1 hour.",
                    from_email=None, # Uses DEFAULT_FROM_EMAIL from settings
                    recipient_list=[self.owner.email],
                    fail_silently=False, # Changed in previous step
                )
                print(f"[EMAIL SUCCESS] SLA Warning email sent for ticket '{self.title}' to {self.owner.email}")
                self.save() # Save after successful email send
            except Exception as e:
                print(f"[EMAIL ERROR] Failed to send SLA Warning email for ticket '{self.title}' to {self.owner.email}. Error: {e}")
                # Similar to above, consider error handling strategy.
                # self.save() to persist sla_warning_sent = True
                self.save()
