# agendamento/views.py
from .models import Medico, Horarios
from datetime import datetime, timedelta

def get_medicos(request):
    servico_id = request.GET.get('servico_id')
    # Aqui você precisaria adaptar para sua lógica de negócios
    medicos = Medico.objects.filter(...)
    return render(...)

def get_horarios(request):
    medico_id = request.GET.get('medico_id')
    data = request.GET.get('data')
    
    # Converter a string da data para objeto date
    data_obj = datetime.strptime(data, '%Y-%m-%d').date()
    
    # Filtrar horários disponíveis
    horarios = Horarios.objects.filter(
        id_medico=medico_id,
        dia__date=data_obj,
        inicio__gte=(datetime.now() + timedelta(hours=1)).time() if data_obj == datetime.now().date() else datetime.min.time()
    ).order_by('inicio')
    
    return render(...)