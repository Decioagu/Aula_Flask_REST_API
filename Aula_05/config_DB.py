import os

# endereço da pasta atual
basedir = os.path.abspath(os.path.dirname(__file__))

# configuração do Banco de Dados
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'banco.db') # tipo de banco
    SQLALCHEMY_TRACK_MODIFICATIONS = False # rastrear modificações em objetos
    JWT_SECRET_KEY = 'DontTellAnyone' # criptografia (token)
    JWT_BLACKLIST_ENABLED  = True # lista negra de token

