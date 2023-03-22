from django.contrib import admin
from .models import Showtime, Movie


class ShowtimeInline(admin.TabularInline):
    model = Showtime
    extra = 1


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    inlines = [ShowtimeInline]
    prepopulated_fields = {'slug': ('title',)}
