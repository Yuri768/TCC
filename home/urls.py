from django.urls import path, include
from django.views.generic.base import RedirectView
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='main'),
]