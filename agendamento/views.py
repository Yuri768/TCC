from django.shortcuts import render
from django.http import JsonResponse

def agendar_consulta(request):
    return render(request, 'agendamento/agendamento.html')

def get_medicos(request):
    # Dados fictícios - substitua por consulta ao banco de dados depois
    servico_id = request.GET.get('servico_id')
    medicos = []
    
    if servico_id == 'cardiologia':
        medicos = [
            {'id': 1, 'nome': 'Dr. Carlos Silva'},
            {'id': 2, 'nome': 'Dra. Ana Souza'}
        ]
    elif servico_id == 'dermatologia':
        medicos = [
            {'id': 3, 'nome': 'Dr. Marcos Oliveira'},
            {'id': 4, 'nome': 'Dra. Juliana Costa'}
        ]
    
    options = '<option value="">Selecione um médico...</option>'
    for medico in medicos:
        options += f'<option value="{medico["id"]}">{medico["nome"]}</option>'
    
    return JsonResponse({'options': options})

def get_horarios(request):
    # Dados fictícios - substitua por consulta ao banco de dados depois
    medico_id = request.GET.get('medico_id')
    data = request.GET.get('data')
    
    horarios = ['08:00', '09:00', '10:00', '11:00', '14:00', '15:00', '16:00']
    
    time_slots = []
    for horario in horarios:
        time_slots.append({
            'id': horario.replace(':', ''),
            'horario': horario
        })
    
    return JsonResponse({'horarios': time_slots})

def AgendarConsultaView(request):
    # Implementação básica - substitua por lógica real depois
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'Agendamento realizado com sucesso!'})
    return JsonResponse({'status': 'error'}, status=400)

def historico_view(request):
    if request.method == 'GET':
        return render(request, 'agendamento/historico.html')