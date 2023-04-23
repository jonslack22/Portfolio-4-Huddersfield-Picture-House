from . import views
from .views import MovieList, BookingDetailView
from django.views.generic import TemplateView
from django.urls import path


urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('whatson', views.MovieList.as_view(), name='whatson'),
    path(
        'booking/<int:pk>/', BookingDetailView.as_view(),
        name='booking_detail'
        ),
    path(
        'managebooking/', views.ManageBookingView.as_view(),
        name='managebooking'
        ),
    path(
        'bookingedit/<int:pk>/', views.BookingEditView.as_view(),
        name='bookingedit'
        ),
    path(
        'bookingsuccess/', views.BookingSuccessView.as_view(),
        name='bookingsuccess'
        ),
    path(
        'deletebooking/<int:pk>/', views.DeleteBookingView.as_view(),
        name='deletebooking'
        ),
    path(
        'deletesuccess/', views.DeleteSuccessView.as_view(),
        name='deletesuccess'
        ),
]
