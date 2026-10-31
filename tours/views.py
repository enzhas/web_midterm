from django.db import DatabaseError, connection
from django.db.models.deletion import ProtectedError
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking, Tour
from .serializers import BookingSerializer, TourSerializer


@api_view(["GET"])
def api_root(request):
    return Response({"name": "Tour Operator API", "tours": request.build_absolute_uri("/api/tours/"), "bookings": request.build_absolute_uri("/api/bookings/"), "health": request.build_absolute_uri("/api/health/")})


@api_view(["GET"])
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DatabaseError:
        return Response({"status": "unavailable"}, status=503)
    return Response({"status": "ok", "database": "postgresql"})


class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response({"detail": "Delete this tour's bookings before deleting the tour."}, status=status.HTTP_409_CONFLICT)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related("tour").all()
    serializer_class = BookingSerializer


def not_found(request, exception):
    return JsonResponse({"detail": "Not found."}, status=404)


def server_error(request):
    return JsonResponse({"detail": "Internal server error."}, status=500)
