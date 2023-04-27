from django.db.models.signals import post_save
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.views import generic, View
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from .models import Movie, ShowTime, Booking


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
    View to render booking detail and allow user to create a booking
    """
    login_url = '/accounts/login/'

    def get(self, request, pk):
        showtime = get_object_or_404(ShowTime, pk=pk)
        booked_seats = Booking.objects.filter(show_time=showtime).values_list('seats', flat=True)
        context = {
            'movie': showtime.movie,
            'showtime': showtime,
            'booked_seats': booked_seats,
            'user': request.user,
        }
        return render(request, 'booking_detail.html', context)

    def post(self, request, pk):
        showtime = get_object_or_404(ShowTime, pk=pk)
        seats = request.POST.getlist('seats')
        booking = Booking(user=request.user, show_time=showtime, seats=seats)
        try:
            booking.full_clean()
        except ValidationError as e:
            context = {
                'movie': showtime.movie,
                'showtime': showtime,
                'booked_seats': Booking.objects.filter(
                    show_time=showtime).values_list('seats', flat=True),
                'user': request.user,
                'errors': e.message_dict,
            }
            return render(request, 'booking_detail.html', context)
        booking.save()
        return redirect('bookingsuccess', pk=booking.pk)


class BookingSuccessView(TemplateView):
    """
    A view to show the booking was successful
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
    template_name = 'booking_edit.html'
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
