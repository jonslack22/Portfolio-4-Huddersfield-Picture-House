from django.contrib import admin
from .models import Movie, Showtime


class ShowtimeInline(admin.TabularInline):
    """
    This class allows the 'Showtime' model to be edited inline
    within the 'Movie' model admin page. An extra form can be
    displayed if multiple showings for a movie are desired.
    """
    model = Showtime
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [ShowtimeInline]
    prepopulated_fields = {'slug': ('title',)}
