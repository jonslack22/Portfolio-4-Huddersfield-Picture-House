from django import forms
from django.core.exceptions import ValidationError
from .models import Booking
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("name", "movie_id", "show_time", "guests", "seats")
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Please enter your name"
            }),
            "movie_id": forms.Select(attrs={
                "class": "form-control",
            }),
            "show_time": forms.Select(attrs={
                "class": "form-control",
            }),
            "guests": forms.Select(attrs={
                "class": "form-control",
            }, choices=[(x, x) for x in range(1, 11)]),
            "seats": forms.SelectMultiple(attrs={
                "class": "form-control",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["movie_id"].queryset = Movie.objects.all()
        self.fields["show_time"].queryset = ShowTime.objects.none()

        if "movie_id" in self.data:
            try:
                movie_id = int(self.data.get("movie_id"))
                self.fields["show_time"].queryset = ShowTime.objects.filter(
                    movie_id=movie_id).order_by("start_time")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["show_time"].queryset = \
                self.instance.movie_id.showtimes.order_by("start_time")
