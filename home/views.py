from django.shortcuts import render, redirect
from accounts.models import Usuario

def home(request):
    usuario_id = request.session.get('usuario_id')

    if usuario_id:
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            return render(request, 'home.html', {'usuario': usuario})
        except Usuario.DoesNotExist:
            # Se o usuário não existir, limpa a sessão e redireciona
            del request.session['usuario_id']
            return render(request, 'home.html')
    else:
        return render(request, 'home.html')