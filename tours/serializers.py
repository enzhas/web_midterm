from rest_framework import serializers
from .models import Booking, Tour


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ["id", "title", "destination", "description", "price", "start_date", "end_date", "max_guests", "is_active"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        start = attrs.get("start_date", getattr(self.instance, "start_date", None))
        end = attrs.get("end_date", getattr(self.instance, "end_date", None))
        if start and end and end < start:
            raise serializers.ValidationError({"end_date": "Must be on or after start_date."})
        return attrs


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["id", "tour", "customer_name", "customer_email", "guests", "status", "notes", "created_at"]
        read_only_fields = ["id", "created_at"]
