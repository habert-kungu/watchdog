from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import (
    Ticket,
)  # Ensure Ticket model exists and is correctly defined in models.py
from .serializers import TicketSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail

# Create your views here.


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket._default_manager.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print("[DEBUG] perform_create called")
        ticket = serializer.save(owner=self.request.user)
        try:
            print(f"[DEBUG] Preparing to send email for new ticket '{ticket.title}' to {self.request.user.email}")
            send_mail(
                subject=f"New Ticket Created: {ticket.title}",
                message=f"A new ticket has been created.\n\nTitle: {ticket.title}\nDescription: {ticket.description}\nDeadline: {ticket.deadline}",
                from_email=None,  # Uses DEFAULT_FROM_EMAIL from settings
                recipient_list=[self.request.user.email],
                fail_silently=False,
            )
            print(f"[EMAIL SUCCESS] New ticket confirmation email sent for '{ticket.title}' to {self.request.user.email}")
        except Exception as e:
            print(f"[EMAIL ERROR] Failed to send new ticket confirmation email for '{ticket.title}' to {self.request.user.email}. Error: {e}")
        self.notification_message = f"Ticket '{ticket.title}' created. Please check your email for confirmation."

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Attach notification message if available
        if (
            hasattr(self, "notification_message")
            and hasattr(response, "data")
            and response.data is not None
        ):
            response.data["notification"] = self.notification_message
        return response


def dashboard(request):
    return render(request, "tickets/dashboard.html")


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")  # Now required
        if not username or not password or not email:
            return Response(
                {"error": "Username, password, and email are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if User._default_manager.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User._default_manager.create_user(
            username=username, password=password, email=email
        )
        token, created = Token._default_manager.get_or_create(user=user)
        return Response(
            {"message": "User registered successfully.", "token": token.key},
            status=status.HTTP_201_CREATED,
        )
    return Response(
        {"error": "Only POST method allowed."},
        status=status.HTTP_405_METHOD_NOT_ALLOWED,
    )
