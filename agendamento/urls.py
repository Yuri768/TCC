# agendamento/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('agendar/', views.agendar_consulta, name='agendar'),
    path('get_medicos/', views.get_medicos, name='get_medicos'),
    path('get_horarios/', views.get_horarios, name='get_horarios'),
]