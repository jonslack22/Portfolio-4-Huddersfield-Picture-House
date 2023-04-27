from django.contrib import admin
from .models import Movie, ShowTime, Booking


class ShowTimeInline(admin.TabularInline):
    model = ShowTime


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [ShowTimeInline]
    list_display = ('title', 'duration_minutes')
