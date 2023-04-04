from django.db.models.signals import post_save
from django.shortcuts import render
from django.dispatch import receiver
from django.views import generic
from .models import Movie, Showtime, Seat


class MovieList(generic.ListView):
    model = Movie
    queryset = Movie.objects.filter().order_by('title')
    template_name = 'whatson.html'
    context_object_name = 'movie_list'


@receiver(post_save, sender=Showtime)
# The @receiver decorator is used to create seats for a newly created Showtime
# object. The post_save signal is sent every time a Showtime object is saved,
# and the create_seats function is called as a receiver of that signal.
def create_seats(sender, instance, created, **kwargs):
    if created:
        # The function creates and saves the related Seat objects to the
        # database.
        seats = []
        for row in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']:
            for number in range(1, 21):
                seats.append(Seat(row=row, number=number))
        Seat.objects.bulk_create(seats)
