from flask import Flask, request ### request no Flask é usado para acessar dados enviados pelo cliente em uma requisição HTTP.
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

# endereço da pasta atual
caminho_do_arquivo = Path(__file__).parent

app = Flask(__name__) # instanciar Flask

# configuração do Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{caminho_do_arquivo}\\banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) # ORM criando uma engine para um banco

"""
class HotelModel(db.Model):
    ".Model" Subclasse para definir modelos de banco de dados (herança).
    (herança) possibilita criação das colunas e tabelas em SQLAlchemy.
"""
# modelo: gerenciamento e validação de dados
class HotelModel(db.Model):
    __tablename__ = 'hoteis'
    hotel_id = db.Column(db.String, primary_key=True)
    nome = db.Column(db.String(80))
    estrelas = db.Column(db.Float(precision=1))
    diaria = db.Column(db.Float(precision=2))
    cidade = db.Column(db.String(40))

    # construtor
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    # exibir
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }

# executada antes de cada solicitação do aplicativo Flask
@app.before_request 
def cria_banco():
    db.create_all()

@app.route('/hoteis', methods=['GET'])
def get_hoteis():
    return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

@app.route('/hotel/<string:hotel_id>', methods=['GET'])
def get_hotel(hotel_id):
    hotel = HotelModel.query.get(hotel_id)
    if hotel:
        return hotel.json()
    return {'mensagem': 'Hotel não encontrado'}, 404

@app.route('/hotel/<string:hotel_id>', methods=['POST'])
def post_hotel(hotel_id):
    dados = request.get_json() ### acessar dados enviados pelo cliente em uma requisição HTTP.
    hotel = HotelModel.query.get(hotel_id)
    if hotel:
            return {'mensagem': 'Hotel já existe.'}, 404
    else:
        novo_hotel = HotelModel(hotel_id, **dados)
        db.session.add(novo_hotel)
        db.session.commit()
        return novo_hotel.json(), 201

@app.route('/hotel/<string:hotel_id>', methods=['PUT'])
def put_hotel(hotel_id):
    dados = request.get_json() ### acessar dados enviados pelo cliente em uma requisição HTTP.
    hotel = HotelModel.query.get(hotel_id)

    if hotel:
        hotel.nome = dados['nome']
        hotel.estrelas = dados['estrelas']
        hotel.diaria = dados['diaria']
        hotel.cidade = dados['cidade']
    else:
        hotel = HotelModel(hotel_id, **dados)
        db.session.add(hotel)
    
    db.session.commit()
    return hotel.json()

@app.route('/hotel/<string:hotel_id>', methods=['DELETE'])
def delete_hotel(hotel_id):
    hotel = HotelModel.query.get(hotel_id)
    if hotel:
        db.session.delete(hotel)
        db.session.commit()
        return {'mensagem': 'Hotel deletado com sucesso'}
    return {'mensagem': 'Hotel não encontrado'}, 404

if __name__ == '__main__':
    app.run(debug=True)
