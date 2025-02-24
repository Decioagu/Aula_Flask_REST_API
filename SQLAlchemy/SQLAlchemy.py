from pathlib import Path ###

# Criando uma engine para um banco SQLite (ou pode ser MySQL, PostgreSQL etc.)
caminho_do_arquivo = Path(__file__).parent
engine = create_engine(f"sqlite:///{caminho_do_arquivo}\meubanco.db", echo=True)

from sqlalchemy import create_engine, Column, Integer, String ###
from sqlalchemy.orm import declarative_base, sessionmaker ###

# Criando um Modelo de Tabela com ORM
Base = declarative_base()
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    idade = Column(Integer, nullable=False)

''' 
### Criando um Modelo de Tabela com ORM ###
Segue equivalência:
    from flask_sqlalchemy import SQLAlchemy == from sqlalchemy.orm import declarative_base
    SQLAlchemy().Model == declarative_base()
'''
# Criando a tabela no banco de dados
Base.metadata.create_all(engine)

# Criando uma Sessão para Interagir com o Banco:
Session = sessionmaker(bind=engine)
session = Session()

# Inserindo Dados:
novo_usuario = Usuario(nome="Alice", idade=25)
session.add(novo_usuario)
session.commit()

# Consultando Dados:
usuarios = session.query(Usuario).all()
for usuario in usuarios:
    print(usuario.nome, usuario.idade)


