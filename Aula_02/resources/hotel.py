from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from dados_hoteis import hoteis

# rotas ler (dados hoteis)
class Hoteis(Resource):
    # Solicitar
    def get(self):
        return {'hoteis': hoteis} # lista (dados hoteis)

# rota (CRUD)
class Hotel(Resource):

    # Dados pre definidos (Construtor Local)
    atributos = reqparse.RequestParser() # requerimento (extrair valores)
    atributos.add_argument('nome', type=str, required=True, help="Falta nome") # argumentos (campo obrigatório)
    atributos.add_argument('estrelas', type=float) # argumentos
    atributos.add_argument('diaria', type=float) # argumentos
    atributos.add_argument('cidade', type=str) # argumentos

    # # Função auxiliar (Filtro)
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return False
    
    # Solicitar (leitura) por "id"
    def get(self, hotel_id): 
        # (Construtor Local).(Filtro (pesquisa por ID)) 
        hotel = Hotel.find_hotel(hotel_id) 

        if hotel:
            return hotel
        else:
            return {'message': 'Hotel não existe.'}, 404
    
    # Enviar (criar)
    def post(self, hotel_id):    
        # dados = (Construtor Local).(argumentos).(extrair valores) 
        dados = Hotel.atributos.parse_args()

        # novo_hotel_objeto = (ESCOPO Flask (hotel_id, (Construtor Local)))
        novo_hotel_objeto = HotelModel(hotel_id, **dados)

        # novo_hotel_dicionario = (ESCOPO Flask).(método json)
        novo_hotel_dicionario = novo_hotel_objeto.json()

        # (Construtor Local).(Filtro (pesquisa por ID)) 
        hotel = Hotel.find_hotel(hotel_id) # retorna alguma coisa ou falso

        # Se ID não existir
        if not hotel:
            hoteis.append(novo_hotel_dicionario)  # Adicionar na lista (dados hoteis)
            return novo_hotel_dicionario, 201
        else:
            return {'message': 'Hotel já existe.'}, 400

    # Atualizar (alterar)
    def put(self, hotel_id):
        # (Construtor Local).(Filtro).(pesquisa por ID )
        dados = Hotel.atributos.parse_args()

        # novo_hotel_objeto = (ESCOPO Flask (hotel_id,  (Construtor Local)))
        novo_hotel_objeto = HotelModel(hotel_id, **dados)

        # novo_hotel_dicionario = (ESCOPO Flask).(método json)
        novo_hotel_dicionario = novo_hotel_objeto.json()
        
        # hotel = (Construtor Local).(Filtro (pesquisa por ID))
        hotel = Hotel.find_hotel(hotel_id) # retorna alguma coisa ou falso
        
        # Se ID existir
        if hotel:
            hotel.update(novo_hotel_dicionario) # Alterar lista (dados hoteis)
            return hotel, 200
        else:
            hoteis.append(novo_hotel_dicionario) # Adicionar lista (dados hoteis)
            return novo_hotel_dicionario, 201

    # Excluir
    def delete(self, hotel_id):

        # hotel = (Construtor Local).(Filtro (pesquisa por ID))
        hotel = Hotel.find_hotel(hotel_id) # retorna alguma coisa ou falso

        # (dados hoteis)
        global hoteis

        # cria uma nova lista excluindo o ID informado
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]

        # Se ID existir
        if hotel:
            return {'message': 'Hotel deletado.'}, 200
        else:
            return {'message': 'Hotel não existe.'}, 400
