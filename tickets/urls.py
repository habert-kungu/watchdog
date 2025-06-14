from rest_framework.routers import DefaultRouter
from .views import TicketViewSet, dashboard
from django.urls import path

router = DefaultRouter()
router.register(r"tickets", TicketViewSet)

urlpatterns = router.urls + [
    path("dashboard/", dashboard, name="dashboard"),
]
