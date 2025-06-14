from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Ticket
from .serializers import TicketSerializer
from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit

# Create your views here.


@method_decorator(
    ratelimit(key="user", rate="10/m", method="GET", block=True), name="list"
)
@method_decorator(
    ratelimit(key="user", rate="5/m", method="POST", block=True), name="create"
)
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]


def dashboard(request):
    return render(request, "tickets/dashboard.html")
