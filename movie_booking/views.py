from datetime import datetime
from django.db.models.signals import post_save
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.views import generic, View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from .forms import BookingForm
from .models import Movie, ShowTime, Booking


def get_available_seats(self):
    # Get all seats
    seats = self.seat_arrangement.split(',')
    # Get seats that are not booked
    bookings = Booking.objects.filter(show_time=self)
    booked_seats = [booking.seat_number for booking in bookings]
    available_seats = [seat for seat in seats if seat not in booked_seats]
    return available_seats


class IndexView(TemplateView):
    """
    View to the landing page
    """

    template_name = "index.html"


class MovieList(generic.ListView):
    model = Movie
    queryset = Movie.objects.filter().order_by("title")
    template_name = "whatson.html"
    context_object_name = "movie_list"


class BookingDetailView(LoginRequiredMixin, View):
    """
    View to render booking detail and allow user to create a booking
    """
    template_name = 'booking_detail.html'

    def get(self, request, pk, showtime_start_time):
        movie = get_object_or_404(Movie, pk=pk)
        showtime = get_object_or_404(
            ShowTime, movie=movie, start_time=showtime_start_time)
        available_seats = get_available_seats(showtime)
        form = BookingForm(showtime=showtime)
        return render(
            request, 'booking_detail.html',
            context={'form': form, 'showtime': showtime})

    def post(self, request, pk, showtime_start_time):
        model = Booking
        form = BookingForm(request.POST)
        showtime = get_object_or_404(
            ShowTime, movie=movie, start_time=showtime_start_time)

        if form.is_valid():
            seats = form.cleaned_data["seats"]
            booking = Booking.objects.create(
                user=request.user, show_time=showtime, seats=seats)
            booking.seats.set(seats)
            booking.save()
            return render(
                    request, 'booking_success.html',
                    {
                        'Booking_made': Booking_made}
                    )
        else:
            errorMessage = "There was a problem with your booking Please "
            "try again."
            return render(
                request, 'booking_detail.html',
                {
                    'form': form,
                    'errorMessage': errorMessage,
                    'showtime': showtime
                }
            )


class BookingSuccessView(TemplateView):
    """
    A view to show the booking was successful
    """

    template_name = "booking_success.html"


class DeleteBookingView(DeleteView):
    """A view to delete a booking"""

    model = Booking
    template_name = "delete_booking.html"
    success_url = "/deletesuccess"


class BookingEditView(UpdateView):
    """
    A view to provide an interface for users to
    edit their booking
    """

    model = Booking
    template_name = "booking_edit.html"
    success_url = "/managebooking"


class ManageBookingView(ListView):
    """
    View to render ManageBookings
    """

    model = Booking
    template_name = "manage_booking.html"


class DeleteSuccessView(TemplateView):
    """
    A view to provide the user with a delete sucess page
    """

    template_name = "delete_success.html"
