from rest_framework import serializers
from .models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            "title",
            "description",
            "deadline",
            "owner",
            "created_at",
            "sla_missed",
            "sla_warning_sent",
        ]
        read_only_fields = ["owner", "created_at", "sla_missed", "sla_warning_sent"]
