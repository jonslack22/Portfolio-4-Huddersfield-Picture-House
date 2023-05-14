from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary.models import CloudinaryField


class Movie(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration_minutes = models.IntegerField()
    age_rating = models.CharField(max_length=3, choices=[
        ('U', 'U'),
        ('PG', 'PG'),
        ('12A', '12A'),
        ('15', '15'),
        ('18', '18'),
    ])
    featured_image = CloudinaryField("image", default="placeholder")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class ShowTime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    seat_arrangement = models.CharField(
        max_length=1000, default=",".join(str(i) for i in range(1, 221))
    )

    def __str__(self):
        return f"{self.movie} - {self.start_time}"


class Booking(models.Model):
    name = models.CharField(max_length=100)
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    show_time = models.ForeignKey(
        ShowTime, on_delete=models.CASCADE, related_name="bookings")
    guests = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])
    seats = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"{self.name} - {self.show_time} - {self.seats}"

    def clean(self):
        super().clean()

        if self.seats > 10:
            raise forms.ValidationError(
        "Maximum of 10 seats allowed per booking")

        if not isinstance(self.seats, int) or self.seats < 1:
            raise forms.ValidationError(
        "Invalid number of seats. You must pick at least 1")

        seats_taken = self.show_time.bookings.aggregate(
            total=Sum('seats'))['total'] or 0
        if seats_taken + self.seats > self.show_time.room.capacity:
            raise forms.ValidationError('Selected seats are not available')

        now = timezone.now()
        show_time = datetime.combine(
            self.show_time.date, self.show_time.start_time)
        if show_time < now + timedelta(hours=1):
            raise forms.ValidationError(
        'Bookings must be made at least one hour in advance')

        return self.cleaned_data
