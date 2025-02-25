from config.sql_alchemy import banco
import requests ###
from flask import request, url_for ###
from dotenv import load_dotenv ###
import os

load_dotenv() ###

MAILGUN_DOMAIN = os.getenv('DOMINIO') ###
MAILGUN_API_KEY = os.getenv('CHAVE') ###
FROM_TITLE = os.getenv('TITULO') ###
FROM_EMAIL = os.getenv('EMAIL') ###

# atributos a ser enviados
class UsuarioModel(banco.Model):
    # ESCOPO Banco de Dados (cls)
    __tablename__ = 'usuarios'
    usuario_id = banco.Column(banco.Integer, primary_key = True, autoincrement=True) # id auto incremento
    login = banco.Column(banco.String(40), nullable=False)
    senha = banco.Column(banco.String(40), nullable=False)
    email = banco.Column(banco.String(80), nullable=False, unique=True) ### e-mail
    ativado =  banco.Column(banco.Boolean, default=False) ### ativação por e-mail
    '''banco.Model é equivalente a declarative_base() do SQLAlchemy'''

    # ESCOPO Flask (Construtor)
    def __init__(self, login, senha, email, ativado): ###
        self.login = login
        self.senha = senha
        self.email = email ###
        self.ativado = ativado ###
       
    # método json (resposta usuário)
    def json(self):
        return {
            'usuario_id': self.usuario_id,
            'login': self.login,
            'email': self.email, ###
            'ativado' : self.ativado ###
        }
    
    # método filtro
    @classmethod # recebe a própria como argumento "cls"
    def filtro_por_id_usuario(cls, usuario_id):

        # filtra Banco de dados e retorna 1º resultado
        usuario = cls.query.filter_by(usuario_id=usuario_id).first()

        if usuario:
            return usuario
        else:
            return False

    # método login
    @classmethod # recebe a própria como argumento "cls"
    def filtro_login_do_usuario(cls, login):
        # filtra Banco de dados e retorna 1º resultado
        usuario = cls.query.filter_by(login=login).first()

        if usuario:
            return usuario
        else:
            return False
        
    ### método login
    @classmethod # recebe a própria como argumento "cls"
    def filtro_por_email(cls, email):
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
        # print(f'Email enviado com sucesso para {FROM_EMAIL}')
        ### link = http://127.0.0.1:5000/ + endpoint (por padrão digitar em minúsculas nome da sua classe)
        link = request.url_root[:-1] + url_for('usuarioativacao', usuario_id=self.usuario_id)
        return requests.post(f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
                    auth=('api', MAILGUN_API_KEY),
                    data={'from': f'{FROM_TITLE} <{FROM_EMAIL}>',
                        'to': self.email,
                        'subject': 'Confirmação de Cadastro.',
                        'html': f'<html><p>"Confirme seu cadastro clicando no link a seguir: <a href="{link}">CONFIRMAR EMAIL</a></p></html>"'
                        })
        

