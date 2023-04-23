from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic, View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from .models import Movie, Showtime, Reservation as Booking


class IndexView(TemplateView):
    """
    View to the landing page
    """
    template_name = 'index.html'


class MovieList(generic.ListView):
    model = Movie
    queryset = Movie.objects.filter().order_by('title')
    template_name = 'whatson.html'
    context_object_name = 'movie_list'


class BookingDetailView(LoginRequiredMixin, View):
    """
    View to render bookingdetail
    and allow user to create a booking
    """
    login_url = '/accounts/login/'

    def get(self, request, pk):
        showtime = get_object_or_404(Showtime, pk=pk)
        booked_seats = Reservation.objects.filter(
            showtime=showtime).values_list(
            'seat_number', flat=True)
        context = {
            'movie': showtime.movie,
            'showtime': showtime,
            'booked_seats': booked_seats,
            'user': request.user,
        }
        return render(request, 'booking_detail.html', context)


class BookingSuccessView(TemplateView):
    """
    A view to show the booking was successfull
    """
    template_name = 'booking_success.html'


class DeleteBookingView(DeleteView):
    """ A view to delete a booking """
    model = Booking
    template_name = 'delete_booking.html'
    success_url = '/deletesuccess'


class BookingEditView(UpdateView):
    """
    A view to provide an interface for users to
    edit their booking
    """
    model = Booking
    template_name = 'booking_edit'
    success_url = '/managebooking'


class ManageBookingView(ListView):
    """
    View to render ManageBookings
    """
    model = Booking
    template_name = 'manage_booking.html'


class DeleteSuccessView(TemplateView):
    """
    A view to provide the user with a delete sucess page
    """
    template_name = 'delete_success.html'
