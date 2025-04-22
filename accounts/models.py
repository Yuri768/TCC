from django.db import models

class Pessoa(models.Model):
    id_pessoa = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, null=False)
    data_nascimento = models.DateTimeField(null=False)
    nome = models.CharField(max_length=255, null=False)
    senha = models.CharField(max_length=255, null=False)
    cpf = models.CharField(max_length=14, null=False)
    type = models.CharField(max_length=7, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'pessoa'

class Usuario(models.Model):
    id_usuario = models.OneToOneField(
        Pessoa,
        on_delete=models.CASCADE,
        primary_key=True,
        db_column='id_usuario'
    )
    data_cadastro = models.DateField(max_length=255, null=False)
    endereco = models.CharField(max_length=255, null=False)

    class Meta:
        managed = False
        db_table = 'usuario'

    # Propriedade para acessar email como se fosse campo direto
    @property
    def email(self):
        return self.id_usuario.email

    # Propriedade para acessar senha como se fosse campo direto
    @property
    def senha(self):
        return self.id_usuario.senha

class Medico(Pessoa):
    crm = models.CharField(max_length=255, null=False)
    id_clinica = models.ForeignKey('Clinica', on_delete=models.SET_NULL, db_column='id_clinica', null=True, blank=True)

    class Meta:
        managed = False  # Adicionado para evitar migrações
        db_table = 'medico'

class Clinica(models.Model):
    id_clinica = models.AutoField(primary_key=True)
    cnpj = models.CharField(max_length=45)
    nome = models.CharField(max_length=45)
    numero = models.CharField(max_length=45)
    Endereco = models.CharField(max_length=45)
    senha = models.CharField(max_length=255)

    class Meta:
        managed = False  # Adicionado para evitar migrações
        db_table = 'clinica'