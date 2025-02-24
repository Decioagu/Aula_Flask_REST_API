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
    site_id = banco.Column(banco.Integer, banco.ForeignKey('site.site_id'))  # Chave estrangeira
    site = banco.relationship('SiteModel', back_populates='hoteis')  # Relacionamento reverso
    '''
    relationship: é uma função do SQLAlchemy que é usada para definir uma relação entre duas tabelas.
    back_populates='__tablename__': Este parâmetro é usado para definir a relação bidirecional.
    '''

    # ESCOPO Flask
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade, site_id):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id # Chave estrangeira

    # método json
    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'site_id' : self.site_id # Chave estrangeira
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
    def update_hotel(self, nome, estrelas, diaria, cidade, site_id):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id # Chave estrangeira

    # método delete
    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()

