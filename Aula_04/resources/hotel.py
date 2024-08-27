from flask_restful import Resource, reqparse
from models.hotel import HotelModel

# rota lista Banco de Dados (TUDO)
class Hoteis(Resource):
    # (Ler)
    def get(self):
        # ler toda lista (coleção ou tabela) do Banco de Dados
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} 

# rota (CRUD)
class Hotel(Resource):
    # Dados pre definidos (Construtor Local)
    atributos = reqparse.RequestParser() # requerimento (extrair dados)
    # extrair atributo de nome 'nome' (campo obrigatório)
    atributos.add_argument('nome', type=str, required=True, help="Falta nome")
    atributos.add_argument('estrelas') # extrair atributo de nome 'estrelas'
    atributos.add_argument('diaria') # extrair atributo de nome 'diaria'
    atributos.add_argument('cidade') # extrair atributo de nome 'cidade'

    # Solicitar (leitura) por "id"
    def get(self, hotel_id):
        # hotel = (ESCOPO Flask).(método filtro (pesquisa por ID))
        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            # (ESCOPO Flask).(método json)
            return hotel.json()   
        else:
            return {'mensagem': 'Hotel não existe.'}, 404

    # Enviar (criar)
    def post(self, hotel_id): 
        # hotel = (ESCOPO Flask).(método filtro (pesquisa por ID))
        hotel = HotelModel.find_hotel(hotel_id) # retorna alguma coisa ou falso

        # Se ID existir
        if hotel:
            return {f'mensagem': 'Hotel {hotel_id} já existe.'}, 500
        else:     
            # dados = (Construtor Local).(argumentos).(extrair dados)
            dados = Hotel.atributos.parse_args() 

            # novo_hotel = (ESCOPO Flask (hotel_id, (Construtor Local))
            novo_hotel = HotelModel(hotel_id, **dados)

            # (ESCOPO Flask).(método salvar dados)
            novo_hotel.save_hotel() 

            # (ESCOPO Flask).(método json)
            return novo_hotel.json()     

    # Atualizar
    def put(self, hotel_id):
        # dados = (Construtor Local).(argumentos).(extrair dados)
        dados = Hotel.atributos.parse_args()

        # hotel = (ESCOPO Flask).(método filtro (pesquisa por ID)) 
        hotel = HotelModel.find_hotel(hotel_id) # retorna alguma coisa ou falso

        # Se ID existir
        if hotel:
            # (ESCOPO Flask).(método atualizar (Construtor Local))
            hotel.update_hotel(**dados) 

            # (ESCOPO Flask).(método salvar dados)
            hotel.save_hotel() 

            # (ESCOPO Flask).(método json)
            return hotel.json(), 200       
        else:
            # novo_hotel = (ESCOPO Flask (hotel_id, (Construtor Local))
            novo_hotel = HotelModel(hotel_id, **dados)    
            
            # (ESCOPO Flask).(método salvar dados)
            novo_hotel.save_hotel() 

            # (ESCOPO Flask).(método json)
            return novo_hotel.json()
        
    # Excluir
    def delete(self, hotel_id):

        # hotel = (ESCOPO Flask).(método filtro (pesquisa por ID)) 
        hotel = HotelModel.find_hotel(hotel_id) # retorna alguma coisa ou falso

        # Se ID existir
        if hotel:
            # (ESCOPO Flask).(método delete)
            hotel.delete_hotel()
            return {'mensagem': 'Hotel deletado.'}, 200   
        else:
            return {'mensagem': 'Hotel não existe.'}, 404
        
        
