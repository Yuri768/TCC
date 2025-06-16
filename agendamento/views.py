from django.shortcuts import render, redirect
from django.http import JsonResponse
from accounts.models import Pessoa, Medico, Usuario

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
        
        usuario_id = request.session.get('usuario_id') 

        if not usuario_id:
            return redirect('accounts:login')

        context = {}
        
        if usuario_id:
            try:
                # Primeiro verifica se a Pessoa existe
                pessoa = Pessoa.objects.get(id_pessoa=usuario_id)
                
                # Cria a estrutura básica do usuário com os dados da Pessoa
                usuario_data = {
                    'nome': pessoa.nome,
                    'email': pessoa.email,
                    'cpf': pessoa.cpf,
                    'data_nascimento': pessoa.data_nascimento.strftime('%d/%m/%Y') if pessoa.data_nascimento else None
                }
                
                # Depois tenta obter o Usuario relacionado para complementar os dados
                try:
                    usuario = Usuario.objects.get(id_usuario=usuario_id)
                    usuario_data.update({
                        'endereco': usuario.endereco,
                        'data_cadastro': usuario.data_cadastro.strftime('%d/%m/%Y') if usuario.data_cadastro else None
                    })
                except Usuario.DoesNotExist:
                    # Se não encontrar o Usuario, usa valores padrão
                    usuario_data.update({
                        'endereco': 'Não informado',
                        'data_cadastro': None
                    })
                    # Remove a sessão pois o usuário está incompleto
                    del request.session['usuario_id']
                    
                context['usuario'] = usuario_data
                    
            except Pessoa.DoesNotExist:
                # Se a Pessoa não existir, limpa a sessão
                del request.session['usuario_id']
        
        return render(request, 'agendamento/historico.html', context)