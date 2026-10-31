from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q, F


class Tour(models.Model):
    title = models.CharField(max_length=160)
    destination = models.CharField(max_length=120)
    description = models.TextField(blank=True, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    start_date = models.DateField()
    end_date = models.DateField()
    max_guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["id"]
        constraints = [
            models.CheckConstraint(condition=Q(price__gte=0), name="tour_price_nonnegative"),
            models.CheckConstraint(condition=Q(max_guests__gte=1), name="tour_guests_positive"),
            models.CheckConstraint(condition=Q(end_date__gte=F("start_date")), name="tour_dates_ordered"),
        ]

    def __str__(self):
        return self.title


class Booking(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.PROTECT, related_name="bookings")
    customer_name = models.CharField(max_length=120)
    customer_email = models.EmailField()
    guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=12, choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")], default="pending")
    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]
        constraints = [models.CheckConstraint(condition=Q(guests__gte=1), name="booking_guests_positive")]

    def __str__(self):
        return f"Booking {self.pk}: {self.customer_name}"
