from flask_restful import Resource, reqparse
from models.hotel import HotelModel # models
from config.sql_alchemy import banco # ORM (Object-Relational Mapping)

# Função de validação personalizada (PARÂMETRO DO USUÁRIO)
def restricao_estrelas(valor):
    valor = float(valor)
    if valor < 0.0 or valor > 5.0:  # Defina o valor mínimo e máximo aqui
        raise (f"Valor deve estar entre 0.0 e 5.0. Recebido: {valor}")
    return valor

# Função de validação personalizada (PARÂMETRO DO USUÁRIO)
def restricao_diaria(valor):
    valor = float(valor)
    if valor < 0.0:  # Defina o valor mínimo e máximo aqui
        raise (f"Valor deve ser maior que 0: {valor}")
    return valor

# rota lista Banco de Dados (TUDO)
class Hoteis(Resource):
    # (Ler)
    def get(self):
        # {'hoteis': [(MÉTODO AUXILIAR JSON) for hotel in (ESCOPO BANCO DE DADOS.filtra_todos)]}
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}, 200

'''
"Resource" é uma classe base do Flask-RESTful usada para 
criar métodos como get(), post(), put(), delete()
'''

# rota (CRUD)
class Hotel(Resource):
    # PARÂMETRO DO USUÁRIO (Construtor Local)
    atributos = reqparse.RequestParser() # parâmetros pre-definidos (argumentos)
    atributos.add_argument('nome', type=str, required=True, help="Falta nome") # argumentos (required=True | campo obrigatório)
    atributos.add_argument('estrelas', type=restricao_estrelas, help="Número de estrelas (entre 0.0 e 5.0)") # argumentos
    atributos.add_argument('diaria', type=restricao_diaria, help="Valor da diaria não pode ser negativo") # argumentos
    atributos.add_argument('cidade', type=str, required=True, help="cidade") # argumentos

    # Solicitar (leitura) por "id"
    def get(self, hotel_id):
        # hotel = (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por ID)).(retornar 1º resultado)
        hotel = HotelModel.query.filter_by(hotel_id=hotel_id).first() # filtro por id

        if hotel:
            # (ESCOPO BANCO DE DADOS).(MÉTODO AUXILIAR JSON)
            return hotel.json(), 200 # transforma dados filtrado por id para JSON
        else:
            return {'mensagem': 'Hotel não existe.'}, 400

    # Enviar (criar)
    def post(self, hotel_id): 
        # hotel = (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por ID)).(retornar 1º resultado)
        hotel = HotelModel.query.filter_by(hotel_id=hotel_id).first() # filtrar lista hotéis por id

        # Se ID existir
        if hotel:
            return {f'mensagem': 'Hotel {hotel_id} já existe.'}, 400
        else:     
            # dados = (PARÂMETRO DO USUÁRIO).(argumentos).(extrair dados)
            dados = Hotel.atributos.parse_args() # (Construtor Local)

            # novo_hotel = (ESCOPO BANCO DE DADOS (hotel_id, (PARÂMETRO DO USUÁRIO))
            novo_hotel = HotelModel(hotel_id, **dados) # >>>>> (MÉTODO AUXILIAR CONSTRUTOR) <<<<<

            # (ESCOPO BANCO DE DADOS).(método salvar dados)
            banco.session.add(novo_hotel)
            banco.session.commit() 

            # (ESCOPO BANCO DE DADOS).(MÉTODO AUXILIAR JSON)
            return novo_hotel.json(), 201     

    # Atualizar
    def put(self, hotel_id):
        # dados = (PARÂMETRO DO USUÁRIO).(argumentos).(extrair dados)
        dados = Hotel.atributos.parse_args()  # (Construtor Local)

        # hotel = (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por ID)).(retornar 1º resultado)
        hotel = HotelModel.query.filter_by(hotel_id=hotel_id).first() # filtrar lista hotéis por id

        # Se ID existir
        if hotel:
            # Atualizar os atributos do hotel
            hotel.nome = dados['nome']
            hotel.estrelas = dados['estrelas']
            hotel.diaria = dados['diaria']
            hotel.cidade = dados['cidade']

            # (ESCOPO BANCO DE DADOS).(método salvar dados)
            banco.session.add(hotel)
            banco.session.commit() 

            # (ESCOPO BANCO DE DADOS).(MÉTODO AUXILIAR JSON)
            return hotel.json(), 200       
        else:
            # novo_hotel = (ESCOPO BANCO DE DADOS (hotel_id, (PARÂMETRO DO USUÁRIO))
            novo_hotel = HotelModel(hotel_id, **dados) # >>>>> MÉTODO AUXILIAR CONSTRUTOR <<<<<   
            
            # (ESCOPO BANCO DE DADOS).(método salvar dados)
            banco.session.add(novo_hotel)
            banco.session.commit() 

            # (ESCOPO BANCO DE DADOS).(MÉTODO AUXILIAR JSON)
            return novo_hotel.json(), 201
        
    # Excluir
    def delete(self, hotel_id):

        # hotel = (ESCOPO BANCO DE DADOS).(método filtro (pesquisa por ID)).(retornar 1º resultado)
        hotel = HotelModel.query.filter_by(hotel_id=hotel_id).first()

        # Se ID existir
        if hotel:
            # (ESCOPO BANCO DE DADOS).(método delete)
            banco.session.delete(hotel)
            banco.session.commit()
            return {'mensagem': 'Hotel deletado.'}, 200
        else:
            return {'mensagem': 'Hotel não existe.'}, 400
        
  