from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from cloudinary.models import CloudinaryField


class Showtime(models.Model):
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE)
    show_date = models.DateField(auto_now=False)
    show_time = models.TimeField(auto_now=False)
    seats_available = models.IntegerField(default=0)
    seats_taken = models.IntegerField(default=0)

    class Meta:
        unique_together = ('movie', 'show_date', 'show_time')

    def __str__(self):
        return f'{self.movie.title} - {self.show_date} - {self.show_time}'

    def save(self, *args, **kwargs):
        # Set seats_available to the total number of seats if it hasn't
        # been set yet.
        if not self.seats_available:
            self.seats_available = 220

        super().save(*args, **kwargs)


class Movie(models.Model):
    title = models.CharField(max_length=200, unique=False)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')
    showings = models.ManyToManyField(Showtime, related_name='movies')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Reservation(models.Model):
    showtime = models.ForeignKey(
        Showtime, on_delete=models.CASCADE, related_name='reservations')
    name = models.CharField(max_length=100)
    seat_number = models.PositiveIntegerField()
    created_on = models.DateTimeField(default=timezone.now)
    email = models.EmailField()
    date = models.DateField()
    time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.showtime} - {self.seat_number} - {self.user.username}'
