from django import forms
from .models import Reservation
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('seats',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'row g-3'
        self.helper.label_class = 'col-md-4 col-form-label'
        self.helper.field_class = 'col-md-6'

    seats = forms.TypedMultipleChoiceField(
        choices=[(str(i), i) for i in range(1, 101)],
        widget=forms.CheckboxSelectMultiple,
        coerce=int,
        label='Select Seats'
    )

    def clean_seats(self):
        selected_seats = self.cleaned_data.get('seats', [])
        if len(selected_seats) > 10:
            raise forms.ValidationError(
                "You cannot book more than 10 seats at once.")
        return selected_seats
