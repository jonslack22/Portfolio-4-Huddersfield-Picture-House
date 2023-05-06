from django import forms
from .models import Booking
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ("seats",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_class = "row g-3"
        self.helper.label_class = "col-md-4 col-form-label"
        self.helper.field_class = "col-md-6"

        available_seats = list(range(1, self.instance.showtime.seat_arrangement + 1))
        self.fields["seats"].choices = [(str(seat), seat) for seat in available_seats]
        self.fields["seats"].widget = forms.CheckboxSelectMultiple()

    def clean_seats(self):
        selected_seats = self.cleaned_data.get("seats", [])
        if len(selected_seats) > 10:
            raise forms.ValidationError(
                "You cannot book more than 10 seats at once."
            )
        return selected_seats
