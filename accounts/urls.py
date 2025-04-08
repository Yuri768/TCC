from django.urls import path, include
from django.views.generic.base import RedirectView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('registrar/', views.registrar, name='registrar'),
    path('logout/', views.logout, name='logout'),
]