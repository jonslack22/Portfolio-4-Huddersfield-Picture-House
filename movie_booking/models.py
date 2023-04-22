from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone
from cloudinary.models import CloudinaryField


class Showtime(models.Model):
    movie = models.ForeignKey(
        'Movie', on_delete=models.CASCADE, related_name='movie_showtimes')
    show_date = models.DateField(auto_now=False)
    show_times = models.TimeField(auto_now=False)
    seats_available = models.IntegerField(default=0)
    seats_taken = models.IntegerField(default=0)

    class Meta:
        unique_together = ('movie', 'show_date', 'show_times')

    def __str__(self):
        return f'{self.movie.title} - {self.show_date} - {self.show_times}'

    def save(self, *args, **kwargs):
        # Set seats_available to the total number of seats if it hasn't
        # been set yet.
        if not self.seats_available:
            self.seats_available = 100

        super().save(*args, **kwargs)

    def book_seat(request, showtime_id, seat_number):
        showtime = get_object_or_404(Showtime, pk=showtime_id)
        # Find the reservation to update or create
        try:
            reservation = Reservation.objects.get(
                showtime=showtime, seat_number=seat_number)
            # If the reservation already exists, don't allow booking
            return HttpResponse('This seat is already booked')
        except Reservation.DoesNotExist:
            # If the reservation doesn't exist, create a new one
            reservation = Reservation(
                showtime=showtime,
                seat_number=seat_number,
                name=request.POST['name'],
                email=request.POST['email'],
                date=showtime.show_date,
                time=showtime.show_time,
                user=request.user
            )
            reservation.save()
            # Update the seats_available and seats_taken fields in the
            # Showtime object
            showtime.seats_available -= 1
            showtime.seats_taken += 1
            showtime.save()
            return HttpResponseRedirect(
                reverse('booking_detail', args=[showtime_id]))


class Movie(models.Model):
    title = models.CharField(max_length=200, unique=False)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')

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
        return f'{self.showtime} - {self.seat} - {self.user.username}'
