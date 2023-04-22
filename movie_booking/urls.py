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
]
