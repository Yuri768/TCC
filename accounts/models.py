from django.db import models

class Pessoa(models.Model):
    email = models.CharField(max_length=255, null=False)
    data_nascimento = models.DateTimeField(null=False)
    nome = models.CharField(max_length=255, null=False)
    senha = models.CharField(max_length=255, null=False)
    cpf = models.CharField(max_length=14, null=False)

    class Meta:
        db_table = 'pessoa'

class Usuario(Pessoa):
    data_cadastro = models.CharField(max_length=255, null=False)
    endereco = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'usuario'

class Medico(Pessoa):
    crm = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'medico'