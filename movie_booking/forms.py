from django import forms
from django.core.exceptions import ValidationError
from .models import Booking
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class BookingForm(forms.ModelForm):
    seat_range_1 = forms.MultipleChoiceField(
        choices=[(x, x) for x in range(
            1, 56)], label="Seats 1 - 55:", required=False)
    seat_range_2 = forms.MultipleChoiceField(
        choices=[(x, x) for x in range(
            56, 111)], label="Seats 56 - 110:", required=False)
    seat_range_3 = forms.MultipleChoiceField(
        choices=[(x, x) for x in range(
            111, 166)], label="Seats 111 - 165:", required=False)
    seat_range_4 = forms.MultipleChoiceField(
        choices=[(x, x) for x in range(
            166, 221)], label="Seats 166 - 220:", required=False)

    movie_id = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        model = Booking
        fields = ("user", "show_time", "seat_range_1", "seat_range_2",
                  "seat_range_3", "seat_range_4", "seats")
        widgets = {
            "user": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": "Please enter your name"}
            ),
            "show_time": forms.HiddenInput(),
            "seats": forms.HiddenInput()
        }

    def __init__(self, showtime, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.show_time = showtime

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "row g-3"
        self.helper.label_class = "col-md-4 col-form-label"
        self.helper.field_class = "col-md-6"

    def clean(self):
        cleaned_data = super().clean()
        seat_range1 = cleaned_data.get('seat_range_1')
        seat_range2 = cleaned_data.get('seat_range_2')
        seat_range3 = cleaned_data.get('seat_range_3')
        seat_range4 = cleaned_data.get('seat_range_4')

        # combine the selected seats from the four ranges
        selected_seats = []
        for seats in [seat_range1, seat_range2, seat_range3, seat_range4]:
            if seats:
                selected_seats.extend(seats)

        # Check that at least one seat has been selected
        if not selected_seats:
            raise forms.ValidationError("Please select at least one seat")

        if len(selected_seats) > 10:
            raise forms.ValidationError(
                "You cannot book more than 10 seats at once."
            )

        # check for conflicts with existing bookings
        for seat in selected_seats:
            if Booking.objects.filter(
                    show_time=self.show_time,
                    seats__contains=str(seat)).exists():
                raise forms.ValidationError(
                    f"Seat {seat} has already been booked."
                )

        cleaned_data['seats'] = selected_seats
        return cleaned_data
