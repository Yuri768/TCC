# TCC

`pip install pymysql`, 
`pip install bcrypt`, 
`pip install validate-docbr`,
`pip install cryptography`


Para migrar o banco de dados é só rodar os seguintes comandos no terminal:

`python manage.py makemigrations` e `python manage.py migrate`


Abrir o espaço virtual:

(Cria o ambiente) `python -m venv venv`
("Ativa" o ambiente) `./venv/Scripts/Activate`


Abrir o servidor:
`python manage.py runserver`


Abrir o servidor de uma forma que outros dispositivos consigam acessar:
`python manage.py runserver 0.0.0.0:8000`