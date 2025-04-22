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
        data_nascimento = request.POST.get('data_nascimento')
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
    
    if not data_nascimento:
        return redirect('/accounts/registrar/?status=8')

                

    #?status=1 (Erro de email, email não é valido)
    #?status=2 (Erro de email, email ja existe)
    #?status=3 (Erro de nome, nome não pode conter numeros)
    #?status=4 (Erro de nome, nome pequeno de mais ou nulo)
    #?status=5 (Erro de cpf, cpf não é valido)
    #?status=6 (Erro de cpf, cpf Já esta cadastrado em uma conta)
    #?status=7 (Erro de senha, senha muito pequena)
    #?status=8 (Erro de data de nascimento, data de nascimento invalida)


    senha_hashed = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    senha_hashed_str = senha_hashed.decode('utf-8')
    
    cpf_formatado = formatandoCPF(cpf)
    cpf = cpf_formatado

    try:
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
            id_usuario=pessoa.id_pessoa,  # Relaciona com a Pessoa
            data_cadastro = timezone.now().date(),
            endereco=endereco
        )

        request.session['usuario_id'] = pessoa.id_pessoa
        return redirect('home:main')
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erro no registro: {str(e)}", exc_info=True)
        return redirect('/accounts/registrar/?status=99')


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