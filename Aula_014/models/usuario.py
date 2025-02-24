from sql_alchemy import banco
import requests
from flask import request, url_for
from dotenv import load_dotenv 
import os

load_dotenv()

MAILGUN_DOMAIN = os.getenv('CODIGO')
MAILGUN_API_KEY = os.getenv('CHAVE')
FROM_TITLE = os.getenv('TITULO')
FROM_EMAIL = os.getenv('ENVIO')

# atributos a ser enviados
class UsuarioModel(banco.Model):
    # ESCOPO Banco de Dados
    __tablename__ = 'usuarios'
    usuario_id = banco.Column(banco.Integer, primary_key = True, autoincrement=True) # id auto incrementado
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True) ###
    ativado =  banco.Column(banco.Boolean, default=False) ###

    # ESCOPO Flask
    def __init__(self, login, senha, email, ativado ):
        self.login = login
        self.senha = senha
        self.email = email ###
        self.ativado = ativado ###
       
    # método json
    def json(self):
        return {
            'usuario_id': self.usuario_id,
            'login': self.login,
            'email': self.email, ###
            'ativado' : self.ativado ###
        }
    
    # método filtro
    @classmethod # recebe a própria como argumento "cls"
    def find_usuario(cls, usuario_id):

        # filtra Banco de dados e retorna 1º resultado
        usuario = cls.query.filter_by(usuario_id=usuario_id).first()

        if usuario:
            return usuario
        else:
            return False
        
    # método login
    @classmethod # recebe a própria como argumento "cls"
    def find_by_login(cls, login):
        # filtra Banco de dados e retorna 1º resultado
        usuario = cls.query.filter_by(login=login).first()

        if usuario:
            return usuario
        else:
            return False
        
    ### método login
    @classmethod # recebe a própria como argumento "cls"
    def find_by_email(cls, email):
        # filtra Banco de dados e retorna 1º resultado
        usuario = cls.query.filter_by(email=email).first()

        if usuario:
            return usuario
        else:
            return False

    # método salvar dados
    def save_usuario(self):
        banco.session.add(self)
        banco.session.commit()

    # método delete
    def delete_usuario(self):
        banco.session.delete(self)
        banco.session.commit()

    ### método envio de email: https://login.mailgun.com/login/
    def envio_de_email(self):
        '''
        P:\REPOSITORIO\PUBLICO\Aula_Flask_REST_API\Aula_08\models:
        class UsuarioAtivacao(Resource)
        
        P:\REPOSITORIO\PUBLICO\Aula_Flask_REST_API\Aula_08\app.py:
        api.add_resource(UsuarioAtivacao, '/ativacao/<int:usuario_id>', endpoint='UsuarioAtivacao')
        '''
        
        # link = http://127.0.0.1:5000/ + endpoint (por padrão digitar em minúsculas nome da sua classe)
        link = request.url_root[:-1] + url_for('usuarioativacao', usuario_id=self.usuario_id)
        return requests.post(f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
                    auth=('api', MAILGUN_API_KEY),
                    data={'from': f'{FROM_TITLE} <{FROM_EMAIL}>',
                        'to': self.email,
                        'subject': 'Confirmação de Cadastro.',
                        'html': f'<html><p>"Confirme seu cadastro clicando no link a seguir: <a href="{link}">CONFIRMAR EMAIL</a></p></html>"'
                        })