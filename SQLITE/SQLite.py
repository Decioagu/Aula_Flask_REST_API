import sqlite3
from pathlib import Path

# Caminho
ROOT_DIR = Path(__file__).parent
DB_NAME = 'banco.db' # nome do banco
DB_FILE = ROOT_DIR / DB_NAME

TABLE_NAME = 'hoteis' # tabela do banco

# conectar o arquivo (criar)
connection = sqlite3.connect(DB_FILE)

# variável de controle (abrir conexão)
cursor = connection.cursor()

# comando SQL (criar tabela)
cria_tabela = f"CREATE TABLE IF NOT EXISTS {TABLE_NAME} \
    (hotel_id TEXT PRIMARY KEY, \
    nome TEXT, \
    estrelas REAL, \
    diaria REAL, \
    cidade TEXT)"

# Criar tabela e colunas SQLite
cursor.execute(cria_tabela)


# lista de informações para o Banco de Dados
lista_cadastro_de_hoteis = [
        {
        'hotel_id': 'alpha',
        'nome': 'Alpha Hotel',
        'estrelas': 4.3,
        'diaria': 420.34,
        'cidade': 'Rio de Janeiro'
        },
        {
        'hotel_id': 'bravo',
        'nome': 'Bravo Hotel',
        'estrelas': 4.4,
        'diaria': 380.90,
        'cidade': 'Santa Catarina'
        },
        {
        'hotel_id': 'charlie',
        'nome': 'Charlie Hotel',
        'estrelas': 3.9,
        'diaria': 320.20,
        'cidade': 'Santa Catarina'
        }
]

# Inserir valores nas colunas da tabela tabela SQLite
sql_01 = (
    f'INSERT INTO {TABLE_NAME} '
    '(hotel_id, nome, estrelas, diaria, cidade) '
    'VALUES  '
    '(:hotel_id, :nome, :estrelas, :diaria, :cidade)' # lista ou tupla
)

# Inserir valores nas colunas da tabela tabela SQLite
try: 
    cursor.executemany(sql_01, lista_cadastro_de_hoteis)
except Exception as e:
    print('Exclua o banco.db e execute o código novamente.')

# Consultar toda da tabela SQLite
cursor.execute(
    f'SELECT * FROM {TABLE_NAME}'
)
for linha in iter(cursor):
    print(linha)

# https://dbeaver.io/download/ (instalar gerenciador de banco de dados)

connection.commit() # adicionar comando na tabela
cursor.close() # Fechar variável de controle
connection.close() # Fechar conexão com arquivo