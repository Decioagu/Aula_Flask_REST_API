from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required


# rota lista Banco de Dados (TUDO): URL/hoteis?cidade=Rio de Janeiro&estrelas_min=4&diaria_max=400
class Hoteis(Resource):
     # Dados pre definidos (Construtor Local)
    meus_atributos = reqparse.RequestParser() # requerimento (extrair argumentos)
    meus_atributos.add_argument('cidade', type=str, default="",location='args') # argumentos
    meus_atributos.add_argument('estrelas_min', type=float, default=0, location='args') # argumentos
    meus_atributos.add_argument('estrelas_max', type=float, default=0, location='args') # argumentos
    meus_atributos.add_argument('diaria_min', type=float, default=0, location='args') # argumentos
    meus_atributos.add_argument('diaria_max', type=float, default=0, location='args') # argumentos
    meus_atributos.add_argument("itens",type=int, default=3, location="args") # argumentos
    meus_atributos.add_argument("pagina",type=int, default=1, location="args") # argumentos
    '''
    location='args': Indica que o argumento deve ser extraído dos parâmetros da ".query" na URL. 
    Ou seja, ele será lido da parte da URL que vem após o ponto de interrogação (?). 
    Por exemplo, em uma URL como http://exemplo.com/api?diaria_max=100, 
    '''

    # método de (Leitura)
    def get(self):

        # meus_filtros = (Construtor Local).(argumentos).(extrair dados)
        meus_filtros = Hoteis.meus_atributos.parse_args()

        # query = (ESCOPO Flask).consulta
        query = HotelModel.query
        
        '''
        ".query": Esse é um atributo que realizar operações de consulta no banco de dados. 
        É uma funcionalidade do SQLAlchemy que permite construir consultas SQL de maneira 
        programática. A partir do ".query", você pode filtrar, ordenar e obter resultados 
        do banco de dados.
        '''

        # filtros de consulta
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
        if meus_filtros["itens"]:
            query = query.filter(meus_filtros["itens"] == meus_filtros["itens"])
        
        # Paginação
        page = meus_filtros['pagina']
        per_page = meus_filtros['itens']
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        
        # resultado_hotel = [objeto.json() for objeto in itens_do_dicionario]
        resultado_hotel = [hotel.json() for hotel in pagination.items] # resultado

        return {
            "hotéis": resultado_hotel, # Lista de hotéis
            "quantidade de itens": pagination.total, # total de itens
            "quantidade de paginas": pagination.pages, # total de paginas
            "pagina atual": int(page) # pagina atual
        }

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
        hotel = HotelModel.filtro_por_id_hotel(hotel_id)

        if hotel:
            # (ESCOPO Flask).(método json)
            return hotel.json()   
        else:
            return {'mensagem': 'Hotel não existe.'}, 404
    
    # Enviar (criar)
    @jwt_required() # necessário token de acesso
    def post(self, hotel_id): 
        # hotel = (ESCOPO Flask).(método filtro (pesquisa por ID))
        hotel = HotelModel.filtro_por_id_hotel(hotel_id) # retorna alguma coisa ou falso

        # Se ID existir
        if hotel:
            return {f'mensagem': 'Hotel {hotel_id} já existe.'}, 404
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
    @jwt_required() # necessário token de acesso
    def put(self, hotel_id):
        # dados = (Construtor Local).(argumentos).(extrair dados)
        dados = Hotel.atributos.parse_args()

        # hotel = (ESCOPO Flask).(método filtro (pesquisa por ID)) 
        hotel = HotelModel.filtro_por_id_hotel(hotel_id) # retorna alguma coisa ou falso

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
        hotel = HotelModel.filtro_por_id_hotel(hotel_id) # retorna alguma coisa ou falso

        # Se ID existir
        if hotel:
            # (ESCOPO Flask).(método delete)
            hotel.delete_hotel()
            return {'mensagem': 'Hotel deletado.'}, 200   
        else:
            return {'mensagem': 'Hotel não existe.'}, 404
        
        
