from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from accounts.models import Pessoa, Medico, Usuario
from django.utils import timezone
import bcrypt
import re
from validate_docbr import CPF
# Create your views here.

def login(request):
    if request.method == 'GET':
        status = request.GET.get('status')
        return render(request, 'login.html', {'status': status})
    elif request.method == 'POST':
        email = request.POST.get('gmail')
        senha = request.POST.get('senha')

        if not validar_email(email):
            return redirect('/accounts/login/?status=1')
    
        if senha != None:
            if len(senha.strip())<=4:
                return redirect('/accounts/login/?status=2')
        else:
            return redirect('/accounts/login/?status=2')
    
        if not Pessoa.objects.filter(email=email).exists():
            return redirect('/accounts/login/?status=3')

        pessoa = Pessoa.objects.get(email=email)

        if bcrypt.checkpw(senha.encode('utf-8'), pessoa.senha.encode('utf-8')):
            request.session['usuario_id'] = pessoa.id_pessoa
            return redirect('home:main')
        else:
            return redirect('/accounts/login/?status=4')
        
    


def registrar(request):
    if request.method == 'GET':
        status = request.GET.get('status')
        return render(request, 'registrar.html', {'status': status})
    elif request.method == 'POST':
        email = request.POST.get('email')
        data_nascimento_str = request.POST.get('data_nascimento')
        nome = request.POST.get('nome')
        senha = request.POST.get('senha')
        cpf = request.POST.get('cpf')
        endereco = request.POST.get('endereco')


    if not validar_email(email):
        return redirect('/accounts/registrar/?status=1')
    
    if Pessoa.objects.filter(email = email).exists():
        return redirect('/accounts/registrar/?status=2')

    
    if bool(re.search(r'\d', nome)):
        redirect('/accounts/registrar/?status=3')

    if nome != None:
        if len(nome.strip()) <= 3:
            return redirect('/accounts/registrar/?status=4')
    else:
        return redirect('/accounts/registrar/?status=4')
    
    cpf_limpo = "".join(filter(str.isdigit, cpf))

    if not CPF().validate(cpf_limpo):
        return redirect('/accounts/registrar/?status=5')

    if Pessoa.objects.filter(cpf = cpf).exists():
        return redirect('/accounts/registrar/?status=6')

    if senha != None:
        if len(senha.strip())<=4:
            return redirect('/accounts/registrar/?status=7')
    else:
        return redirect('/accounts/registrar/?status=7')
    
    if not data_nascimento_str:
        return redirect('/accounts/registrar/?status=8')

    try:
        senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        senha_hashed_str = senha_hashed.decode('utf-8')
        
        cpf_formatado = formatandoCPF(cpf)
        cpf = cpf_formatado

        data_nascimento = datetime.strptime(data_nascimento_str, '%Y-%m-%d').date()

        # 1. Cria a Pessoa
        pessoa = Pessoa.objects.create(
            email=email,
            data_nascimento=data_nascimento,
            nome=nome,
            senha=senha_hashed_str,
            cpf=cpf,
            type='USUARIO'
        )

        # 2. Cria o Usuario relacionado
        usuario = Usuario.objects.create(
            id_usuario=pessoa,
            endereco=endereco
        )

        request.session['usuario_id'] = pessoa.id_pessoa
        return redirect('home:main')
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erro no registro: {str(e)}", exc_info=True)
        # Adicione isto para debug temporário
        print(f"ERRO DETALHADO: {str(e)}")
        return redirect('/accounts/registrar/?status=99')


def minha_conta(request):

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
    
    return render(request, 'conta_usuario.html', context)

def logout(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']
    return redirect('home:main')


def validar_email(email):
    regex1 = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    regex2 = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\.[a-zA-Z]{2,}$'
    if re.match(regex1, email) or re.match(regex2, email):
        return True
    
    return False

def formatandoCPF(cpf):
    cpf_limpo = "".join(filter(str.isdigit, cpf))
    cpf_formatado = CPF().mask(cpf_limpo)
    return cpf_formatado