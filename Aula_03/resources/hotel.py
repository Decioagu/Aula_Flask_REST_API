from flask_restful import Resource, reqparse

# (dados hoteis)
hoteis = [
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

# rota ler (dados hoteis)
class Hoteis(Resource):
    # Solicitar
    def get(self):
        return {'hoteis': hoteis} # lista (dados hoteis) 

# rota (CRUD)
class Hotel(Resource):

    # Dados pre definidos (Construtor Local)
    atributos = reqparse.RequestParser() # requerimento (extrair valores)
    atributos.add_argument('nome') # extrair atributo de nome 'nome'
    atributos.add_argument('estrelas') # extrair atributo de nome 'estrelas'
    atributos.add_argument('diaria') # extrair atributo de nome 'diaria'
    atributos.add_argument('cidade') # extrair atributo de nome 'cidade'

    # Função auxiliar (Filtro)
    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return False
    
    # Solicitar (leitura) por "id"
    def get(self, hotel_id): 
        # hotel = (Construtor Local).(Filtro (pesquisa por ID)) 
        hotel = Hotel.find_hotel(hotel_id) 

        if hotel:
            return hotel
        else:
            return {'message': 'Hotel não existe.'}, 404
    
    # Enviar (criar)
    def post(self, hotel_id):    
        # dados = (Construtor Local).(argumentos).(extrair valores)
        dados = Hotel.atributos.parse_args()

        # novo_hotel = {hotel_id, (Construtor Local)}
        novo_hotel = {'hotel_id': hotel_id, **dados}
        # ========================= ou ===========================
        # novo_hotel = {
        #     'hotel_id': hotel_id, # envio pelo header do POST
        #     'nome': dados['nome'],
        #     'estrelas': dados['estrelas'],
        #     'diaria': dados['diaria'],
        #     'cidade': dados['cidade']
        # }
        # ========================================================

        # hotel = (Construtor Local).(Filtro (pesquisa por ID))
        hotel = Hotel.find_hotel(hotel_id) # retorna alguma coisa ou falso

        # Se ID não existir
        if not hotel:
            hoteis.append(novo_hotel)  # Adicionar na lista (dados hoteis)
            return novo_hotel, 201
        else:
            return {'message': 'Hotel já existe.'}, 400

    # Atualizar (alterar)
    def put(self, hotel_id):
        # dados = (Construtor Local).(Filtro (pesquisa por ID))
        dados = Hotel.atributos.parse_args()

        # novo_hotel = {hotel_id, (Construtor Local)}
        novo_hotel = {'hotel_id': hotel_id, **dados}
        
        # (Construtor Local).(Filtro (pesquisa por ID))
        hotel = Hotel.find_hotel(hotel_id) # retorna alguma coisa ou falso
        
        # Se ID existir
        if hotel:
            hotel.update(novo_hotel) # Alterar lista (dados hoteis)
            return hotel, 200
        else:
            hoteis.append(novo_hotel) # Adicionar lista (dados hoteis)
            return novo_hotel, 201

    # Excluir 
    def delete(self, hotel_id):

        # hotel = (Construtor Local).(Filtro (pesquisa por ID)) 
        hotel = Hotel.find_hotel(hotel_id) # retorna alguma coisa ou falso

        # (dados hoteis)
        global hoteis

        # cria uma nova lista de hoteis excluindo o ID informado
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]

        # Se ID existir
        if hotel:
            return {'message': 'Hotel deletado.'}, 204
        else:
            return {'message': 'Hotel não existe.'}, 400
