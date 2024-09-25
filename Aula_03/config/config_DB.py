from pathlib import Path
import os

# endereço da pasta atual
caminho_do_arquivo = Path(__file__) # ver caminho do arquivo executado
basedir = os.path.abspath(os.path.dirname(caminho_do_arquivo.parent))

# configuração do Banco de Dados
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'banco.db') # endereço de conexão
    SQLALCHEMY_TRACK_MODIFICATIONS = False

'''
Outras configurações:
    'sqlite:///nome_do_banco'
    'mysql://username:password@localhost:3306/nome_do_banco'
    'postgresql://username:password@localhost:5432/nome_do_banco'
'''