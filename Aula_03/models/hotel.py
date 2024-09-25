from config.sql_alchemy import banco # ORM (Object-Relational Mapping)

# atributos a ser enviados
"""
class HotelModel(banco.Model):
    ".Model" Subclasse para definir modelos de banco de dados (herança).
    (herança) possibilita criação das colunas e tabelas em SQLAlchemy.
"""
# modelo: gerenciamento e validação de dados
class HotelModel(banco.Model):
    # ESCOPO BANCO DE DADOS
    __tablename__ = 'hoteis'
    hotel_id = banco.Column(banco.String, primary_key = True) # id str via Hesders  
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))
    '''
    O argumento precision=1 define a precisão de número de ponto flutuante em 
    casa decimais que serão armazenadas. Neste caso uma casa decimal: exp: 1.0
    '''

    # MÉTODO AUXILIAR JSON ( .resources\hotel.py = GET)
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }

    # MÉTODO AUXILIAR CONSTRUTOR (.resources\hotel.py = POST)
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade




