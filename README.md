# TCC

Esse projeto esta sendo desenvolvido usando python com django, mysql, html, css e javascript.



Abrir o espaço virtual:

(Cria o ambiente) `python -m venv venv`
("Ativa" o ambiente) `./venv/Scripts/Activate`



Instalando todas as bibliotecas necessarias:


`pip install django, pymysql, bcrypt, validate-docbr, cryptography`



Para migrar o banco de dados é só rodar os seguintes comandos no terminal:

`python manage.py migrate auth`, 
`python manage.py migrate admin`,
`python manage.py migrate contenttypes`,
`python manage.py migrate sessions`,
`python manage.py makemigrations agendamento`,
`python manage.py migrate agendamento --fake`,
`python manage.py makemigrations --check`


Abrir o servidor:
`python manage.py runserver`


Abrir o servidor de uma forma que outros dispositivos consigam acessar:
`python manage.py runserver 0.0.0.0:8000`