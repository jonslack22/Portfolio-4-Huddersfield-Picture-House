from django.db import models
from cloudinary.models import CloudinaryField


class Movie(models.Model):
    title = models.CharField(max_length=200, unique=False)
    slug = models.SlugField(unique=True)
    featured_image = CloudinaryField('image', default='placeholder')
    description = models.TextField()
    show_date = models.DateField()
    show_times = models.TimeField()

    class Meta:
        ordering = ['show_times']

    def __str__(self):
        return self.title
