from django.shortcuts import render, redirect
from accounts.models import Usuario, Pessoa

def home(request):
    usuario_id = request.session.get('usuario_id')
    
    context = {}
    
    if usuario_id:
        try:
            # Primeiro verifica se a Pessoa existe
            pessoa = Pessoa.objects.get(id_pessoa=usuario_id)
            
            # Depois tenta obter o Usuario relacionado
            try:
                usuario = Usuario.objects.get(id_usuario=usuario_id)
                context['usuario'] = {
                    'nome': pessoa.nome,
                    'email': pessoa.email,
                    'endereco': usuario.endereco,
                    'data_cadastro': usuario.data_cadastro.strftime('%d/%m/%Y') if usuario.data_cadastro else None
                }
            except Usuario.DoesNotExist:
                # Se não encontrar o Usuario, mantém apenas os dados básicos da Pessoa
                context['usuario'] = {
                    'nome': pessoa.nome,
                    'email': pessoa.email,
                    'endereco': 'Não informado',
                }
                # Remove a sessão pois o usuário está incompleto
                del request.session['usuario_id']
                
        except Pessoa.DoesNotExist:
            # Se a Pessoa não existir, limpa a sessão
            del request.session['usuario_id']
    
    return render(request, 'home.html', context)