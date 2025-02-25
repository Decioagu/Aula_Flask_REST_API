from config.sql_alchemy import banco

# modelo: gerenciamento e validação de dados
class HotelModel(banco.Model):
    # ESCOPO Banco de Dados
    __tablename__ = 'hoteis'
    hotel_id = banco.Column(banco.String, primary_key = True) # id str via Hesders
    nome = banco.Column(banco.String(80), nullable=False)
    estrelas = banco.Column(banco.Float(precision=1), nullable=False)
    diaria = banco.Column(banco.Float(precision=2), nullable=False)
    cidade = banco.Column(banco.String(40), nullable=False)
    site_id = banco.Column(banco.Integer, banco.ForeignKey('site.site_id'), nullable=False)  ### Chave estrangeira
    site = banco.relationship('SiteModel', back_populates='hoteis')  # Relacionamento reverso
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
            'cidade': self.cidade,
            'site_id' : self.site_id # Chave estrangeira
        }

    # MÉTODO AUXILIAR CONSTRUTOR (.resources\hotel.py = POST)
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade, site_id):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id # Chave estrangeira
    
    # método filtro
    @classmethod # recebe a própria como argumento "cls"
    def filtro_por_id_hotel(cls, hotel_id):

        # filtra Banco de dados e retorna 1º resultado
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()

        if hotel:
            return hotel
        else:
            return False

    # método atualizar
    def update_hotel(self, nome, estrelas, diaria, cidade, site_id):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.site_id = site_id # Chave estrangeira

        # método salvar dados
    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    # método delete
    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()

