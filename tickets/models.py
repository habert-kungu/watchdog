from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils import timezone


class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="tickets"
    )
    sla_missed = models.BooleanField(default=False)
    sla_warning_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_owner_email(self):
        # Get the user directly from the database
        User = get_user_model()
        try:
            user = User.objects.select_related().get(pk=self.owner.pk)
            return user.email
        except Exception:
            return None

    def check_and_notify_sla(self):
        current_time = timezone.now()
        deadline_time = timezone.localtime(self.deadline)
        owner_email = self.owner_email

        if not owner_email:
            return

        if not self.sla_missed and current_time > deadline_time:
            self.sla_missed = True
            try:
                print(
                    f"[DEBUG] Preparing to send SLA Missed email for ticket '{self.title}'"
                )
                email_subject = f"🚨 Attention Required: {self.title} needs your immediate attention!"
                email_message = f"""
⚡ URGENT ACTION NEEDED ⚡
========================

Hello there! 👋

🔔 We noticed that the ticket "{self.title}" has missed its SLA deadline.

📋 Ticket Details:
----------------
✨ Title: {self.title}
⏰ Original Deadline: {deadline_time.strftime('%B %d, %Y at %I:%M %p')}
⌛ Time Elapsed: {timezone.localtime(current_time).strftime('%B %d, %Y at %I:%M %p')}

🎯 Required Actions:
-----------------
1. 🔍 Review ticket details
2. 📝 Update the status
3. 🤝 Coordinate with team if needed
4. 🚀 Expedite resolution

💫 Quick Access:
-------------
🌐 Dashboard: Check your dashboard for full details
📱 Mobile: Use our mobile view for on-the-go updates
🔄 Status: Update directly from the ticket page

💡 Pro Tips:
----------
• Fast response = Happy customers! 🌟
• Need help? Your team is just a message away! 💪
• Document any blockers for better tracking 📊

Keep up the amazing work! 🌈

Best wishes,
🤖 Your Friendly Watchdog Team

P.S. Remember: Every resolved ticket makes our customers smile! 🎉
"""
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=None,
                    recipient_list=[owner_email],
                    fail_silently=False,
                )
                print(
                    f"[EMAIL SUCCESS] SLA Missed email sent for ticket '{self.title}'"
                )
                self.save()
            except Exception as e:
                print(
                    f"[EMAIL ERROR] Failed to send SLA Missed email for ticket '{self.title}'. Error: {e}"
                )
                self.save()

        elif (
            not self.sla_warning_sent
            and (deadline_time - current_time).total_seconds() < 3600
            and current_time < deadline_time
        ):
            self.sla_warning_sent = True
            try:
                remaining_minutes = int(
                    (deadline_time - current_time).total_seconds() / 60
                )
                print(
                    f"[DEBUG] Preparing to send SLA Warning email for ticket '{self.title}'"
                )

                email_subject = (
                    f"⏰ Time Alert: {self.title} - Let's Beat the Clock! 🎯"
                )
                email_message = f"""
✨ SLA Countdown Alert! ✨
========================

Hey there, Ticket Hero! 🦸‍♂️

⏳ Time Check: Only {remaining_minutes} minutes remaining! 

🎫 Ticket Snapshot:
-----------------
🌟 Title: {self.title}
📝 Description: {str(self.description)[:100]}{"..." if len(str(self.description)) > 100 else ""}
⏰ Deadline: {deadline_time.strftime('%B %d, %Y at %I:%M %p')}
🕒 Current Time: {timezone.localtime(current_time).strftime('%B %d, %Y at %I:%M %p')}

🚀 Action Station:
---------------
1. 🔍 Quick Review Time!
2. 📊 Status Update Needed?
3. 🏃‍♂️ Sprint to the Finish!
4. 🤝 Need Help? We're Here!

💫 Power Tips:
-----------
• 🎯 Focus Mode: This ticket is your priority
• 🗣️ Communication is key
• 📱 Mobile dashboard available
• ⚡ Quick actions can save the day

You're doing great! Let's wrap this up before the deadline! 🎉

Keep rocking! 🌟
Your Watchdog Team 🐕

P.S. Race against time, but keep that quality high! 💪
P.P.S. You're awesome - you've got this! 🌈
"""
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=None,
                    recipient_list=[owner_email],
                    fail_silently=False,
                )
                print(
                    f"[EMAIL SUCCESS] SLA Warning email sent for ticket '{self.title}'"
                )
                self.save()
            except Exception as e:
                print(
                    f"[EMAIL ERROR] Failed to send SLA Warning email for ticket '{self.title}'. Error: {e}"
                )
                self.save()
