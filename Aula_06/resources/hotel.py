from flask_restful import Resource, reqparse
from models.site import SiteModel
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required



# rota PATH: /hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400&site=1
class Hoteis(Resource):

    # Dados pre definidos (Construtor Local)
    path_params = reqparse.RequestParser() # requerimento (extrair argumentos)
    path_params.add_argument('cidade', type=str, default=None ,location='args') # argumentos
    path_params.add_argument('estrelas_min', type=float, default=0, location='args') # argumentos
    path_params.add_argument('estrelas_max', type=float, default=0, location='args') # argumentos
    path_params.add_argument('diaria_min', type=float, default=0, location='args') # argumentos
    path_params.add_argument('diaria_max', type=float, default=0, location='args') # argumentos
    path_params.add_argument("site", type=float, default=None , location="args") # argumentos
    path_params.add_argument("itens", type=float, default=3, location="args") # argumentos
    path_params.add_argument("pagina", type=float, default=1, location="args") # argumentos
    
    '''
    location='args': Indica que o argumento deve ser extraído dos parâmetros da ".query" na URL. 
    Ou seja, ele será lido da parte da URL que vem após o ponto de interrogação (?). 
    Por exemplo, em uma URL como http://exemplo.com/api?diaria_max=100, 
    '''

    # método de (Leitura)
    def get(self):
        meus_filtros = Hoteis.path_params.parse_args()

        '''
        ".query": Esse é um atributo que realizar operações de consulta no banco de dados. 
        É uma funcionalidade do SQLAlchemy que permite construir consultas SQL de maneira 
        programática. A partir do ".query", você pode filtrar, ordenar e obter resultados 
        do banco de dados.
        '''
        query = HotelModel.query # pesquisar por

        # filtros
        if meus_filtros["cidade"]:
            query = query.filter(HotelModel.cidade == meus_filtros["cidade"])
        if meus_filtros["estrelas_min"]:
            query = query.filter(HotelModel.estrelas >= meus_filtros["estrelas_min"])
        if meus_filtros["estrelas_max"]:
            query = query.filter(HotelModel.estrelas <= meus_filtros["estrelas_max"])
        if meus_filtros["diaria_min"]:
            query = query.filter(HotelModel.diaria >= meus_filtros["diaria_min"])
        if meus_filtros["diaria_max"]:
            query = query.filter(HotelModel.diaria <= meus_filtros["diaria_max"])
        if meus_filtros["site"]:
            query = query.filter(HotelModel.site_id == meus_filtros["site"])
        if meus_filtros["itens"]:
            query = query.filter(meus_filtros["itens"] == meus_filtros["itens"])
        
        # Paginação
        page = meus_filtros['pagina']
        per_page = meus_filtros['itens']
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        # resultado
        resultado_hotel = [hotel.json() for hotel in pagination.items]

        return {
            "hotéis": resultado_hotel,
            "quantidade de itens": pagination.total,
            "quantidade de paginas": pagination.pages,
            "pagina atual": int(page)
        }

# rota (CRUD)
class Hotel(Resource):
    # Dados pre definidos (Construtor Local)
    atributos = reqparse.RequestParser() # requerimento (extrair argumento)
    atributos.add_argument('nome', type=str, required=True, help="Falta nome") # argumentos (campo obrigatório)
    atributos.add_argument('estrelas', type=float) # argumentos
    atributos.add_argument('diaria', type=float) # argumentos
    atributos.add_argument('cidade', type=str) # argumentos
    atributos.add_argument('site_id', type=int, required=True, help="Falta id do site") # argumentos (campo obrigatório)

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
    @jwt_required() # necessário token de acesso
    def post(self, hotel_id): 
        # hotel = (ESCOPO Flask).(método filtro (pesquisa por ID))
        hotel = HotelModel.find_hotel(hotel_id) # retorna alguma coisa ou falso

        # Se ID existir
        if hotel:
            return {f'mensagem': 'Hotel {hotel_id} já existe.'}, 500
        else:     
            # dados = (Construtor Local).(argumentos).(extrair dados)
            dados = Hotel.atributos.parse_args() 

            print(dados)
            # novo_hotel = (ESCOPO Flask (hotel_id, (Construtor Local))
            novo_hotel = HotelModel(hotel_id, **dados)

            # SE não existir site_id cadastrado finalize
            if not SiteModel.find_by_id(dados.get('site_id')):
                return {'mensagem': 'Para cadastra hotel é necessário site_id valido'}, 400

            # (ESCOPO Flask).(método salvar dados)
            novo_hotel.save_hotel() 

            # (ESCOPO Flask).(método json)
            return novo_hotel.json()        

    # Atualizar
    @jwt_required() # necessário token de acesso
    def put(self, hotel_id):
        # dados = (Construtor Local).(argumentos).(extrair dados)
        dados = Hotel.atributos.parse_args()

        print(dados)
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
    @jwt_required() # necessário token de acesso
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
        
        
