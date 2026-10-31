from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TourViewSet, BookingViewSet, health
router = DefaultRouter()
router.register("tours", TourViewSet)
router.register("bookings", BookingViewSet)
urlpatterns = [path("health/", health), path("", include(router.urls))]
