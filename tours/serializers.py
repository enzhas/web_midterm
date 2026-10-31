from rest_framework import serializers
from .models import Booking, Tour


class TourFilterSerializer(serializers.Serializer):
    destination = serializers.CharField(required=False, max_length=120)
    is_active = serializers.BooleanField(required=False)
    min_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2, min_value=0)
    max_price = serializers.DecimalField(required=False, max_digits=10, decimal_places=2, min_value=0)
    ordering = serializers.ChoiceField(required=False, choices=["price", "-price", "start_date", "-start_date", "title", "-title"])

    def validate(self, attrs):
        if "min_price" in attrs and "max_price" in attrs and attrs["min_price"] > attrs["max_price"]:
            raise serializers.ValidationError({"max_price": "Must be greater than or equal to min_price."})
        return attrs


class BookingFilterSerializer(serializers.Serializer):
    tour = serializers.IntegerField(required=False, min_value=1)
    status = serializers.ChoiceField(required=False, choices=Booking._meta.get_field("status").choices)


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
