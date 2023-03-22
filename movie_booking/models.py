from django.db import models
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
