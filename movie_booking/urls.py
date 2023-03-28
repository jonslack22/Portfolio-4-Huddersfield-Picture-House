from .views import MovieList
from django.urls import path


urlpatterns = [
    path('', MovieList.as_view(), name='whatson')
]
