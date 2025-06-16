from django.urls import path
from .views import agendar_consulta, get_medicos, get_horarios, AgendarConsultaView, historico_view

app_name = 'agendamento'

urlpatterns = [
    path('', agendar_consulta, name='agendar'),
    path('get_medicos/', get_medicos, name='get_medicos'),
    path('get_horarios/', get_horarios, name='get_horarios'),
    path('confirmar/', AgendarConsultaView, name='confirmar'),
    path('historico/', historico_view , name='historico')
]