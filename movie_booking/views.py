from django.shortcuts import render
from django.views import generic
from .models import Movie, Showtime


class MovieList(generic.ListView):
    model = Movie
    queryset = Movie.objects.filter().order_by('title')
    template_name = 'whatson.html'
    context_object_name = 'movie_list'
