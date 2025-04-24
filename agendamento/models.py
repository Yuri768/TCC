# agendamento/models.py
from atexit import register
from django.db import models

class Clinica(models.Model):
    id_clinica = models.AutoField(primary_key=True)
    cnpj = models.CharField(max_length=45)
    nome = models.CharField(max_length=45)
    numero = models.CharField(max_length=45)
    Endereco = models.CharField(max_length=45)
    senha = models.CharField(max_length=255)

    class Meta:
        managed = False  # Indica que o Django não gerencia esta tabela
        db_table = 'clinica'  # Nome exato da tabela no banco

class Pessoa(models.Model):
    id_pessoa = models.AutoField(primary_key=True)
    email = models.CharField(max_length=45)
    data_nascimento = models.DateField()
    nome = models.CharField(max_length=45)
    senha = models.CharField(max_length=255)
    cpf = models.CharField(max_length=45)
    type = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pessoa'

class Medico(models.Model):
    id_pessoa = models.OneToOneField(
        'Pessoa',
        on_delete=models.DO_NOTHING,
        db_column='id_pessoa',
        primary_key=True
    )
    crm = models.CharField(max_length=45)
    id_clinica = models.ForeignKey(
        'Clinica',
        db_column='id_clinica',
        on_delete = models.PROTECT,  # Mude para PROTECT ao invés de SET_NULL
        null=False,  # Agora compatível com on_delete=PROTECT
        blank=True
    )

    class Meta:
        managed = False
        db_table = 'medico'
        
class Usuario(models.Model):
    id_usuario = models.OneToOneField(
        'Pessoa',
        on_delete=models.DO_NOTHING,
        db_column='id_usuario',
        primary_key=True
    )
    data_cadastro = models.DateField(auto_now_add=True)
    endereco = models.CharField(max_length=45)

    class Meta:
        db_table = 'usuario'
        managed = False

class Horarios(models.Model):
    id_horario = models.AutoField(primary_key=True)
    id_medico = models.ForeignKey(Medico, models.DO_NOTHING, db_column='id_medico')
    dia = models.DateTimeField()
    inicio = models.TimeField()
    fim = models.TimeField()

    class Meta:
        managed = False
        db_table = 'horarios'