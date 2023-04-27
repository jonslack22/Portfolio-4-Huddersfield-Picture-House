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
    featured_image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return self.title


class ShowTime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.movie} - {self.start_time}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show_time = models.ForeignKey(ShowTime, on_delete=models.CASCADE)
    seats = models.IntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.user} - {self.show_time} - {self.seats}"

    def validate_seats(self):
        if not isinstance(self.seats, int) or self.seats < 1:
            raise ValidationError("Invalid number of seats")
