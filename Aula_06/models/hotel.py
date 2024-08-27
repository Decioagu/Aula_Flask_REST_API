from sql_alchemy import banco

# atributos a ser enviados
class HotelModel(banco.Model):
    # ESCOPO Banco de Dados
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

    # ESCOPO Flask
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    # método json
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade
        }
    
    # método filtro
    @classmethod # recebe a própria como argumento "cls"
    def find_hotel(cls, hotel_id):

        # filtra Banco de dados e retorna 1º resultado
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()

        if hotel:
            return hotel
        else:
            return False

    # método salvar dados
    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    # método atualizar
    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    # método delete
    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()

