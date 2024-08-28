from dotenv import load_dotenv 
import os

load_dotenv()

nome_do_banco_de_dados = os.getenv('NOME_DO_BANCO')

# endereço da pasta atual
basedir = os.path.abspath(os.path.dirname(__file__))

# configuração do Banco de Dados
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, nome_do_banco_de_dados) # tipo de banco
    SQLALCHEMY_TRACK_MODIFICATIONS = False # rastrear modificações em objetos
    JWT_SECRET_KEY = 'DontTellAnyone' # criptografia (token)
    JWT_BLACKLIST_ENABLED  = True # lista negra de token

'''
'sqlite:///nome_do_banco'
'mysql://username:password@localhost:3306/nome_do_banco'
'postgresql://username:password@localhost:5432/nome_do_banco'
'''