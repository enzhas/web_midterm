from django.db import DatabaseError, connection
from django.db.models.deletion import ProtectedError
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking, Tour
from .serializers import BookingSerializer, TourSerializer, TourFilterSerializer, BookingFilterSerializer


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

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != "list":
            return queryset
        query = TourFilterSerializer(data=self.request.query_params)
        query.is_valid(raise_exception=True)
        params = query.validated_data
        for parameter, lookup in [("destination", "destination__icontains"), ("is_active", "is_active"), ("min_price", "price__gte"), ("max_price", "price__lte")]:
            if parameter in params:
                queryset = queryset.filter(**{lookup: params[parameter]})
        if "ordering" in params:
            queryset = queryset.order_by(params["ordering"], "id")
        return queryset

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response({"detail": "Delete this tour's bookings before deleting the tour."}, status=status.HTTP_409_CONFLICT)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related("tour").all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != "list":
            return queryset
        query = BookingFilterSerializer(data=self.request.query_params)
        query.is_valid(raise_exception=True)
        params = query.validated_data
        if "tour" in params:
            queryset = queryset.filter(tour_id=params["tour"])
        if "status" in params:
            queryset = queryset.filter(status=params["status"])
        return queryset


def not_found(request, exception):
    return JsonResponse({"detail": "Not found."}, status=404)


def server_error(request):
    return JsonResponse({"detail": "Internal server error."}, status=500)
