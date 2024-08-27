import os

# endereço da pasta atual
basedir = os.path.abspath(os.path.dirname(__file__))

# configuração do Banco de Dados
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'banco.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

