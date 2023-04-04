from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Showtime(models.Model):
    movie = models.ForeignKey(
        'Movie', on_delete=models.CASCADE, related_name='movie_showtimes')
    show_date = models.DateField(auto_now=False)
    show_times = models.TimeField(auto_now=False)

    class Meta:
        unique_together = ('movie', 'show_date', 'show_times')

    def __str__(self):
        return f'{self.movie.title} - {self.show_date} - {self.show_times}'


class Movie(models.Model):
    title = models.CharField(max_length=200, unique=False)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    featured_image = CloudinaryField('image', default='placeholder')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Seat(models.Model):
    row = models.CharField(max_length=1)
    number = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('row', 'number')

    def __str__(self):
        return f'{self.row}{self.number}'


class Reservation(models.Model):
    showtime = models.ForeignKey(
        Showtime, on_delete=models.CASCADE, related_name='reservations')
    seat = models.ForeignKey(
        Seat, on_delete=models.CASCADE, related_name='reservations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.showtime} - {self.seat} - {self.user.username}'
