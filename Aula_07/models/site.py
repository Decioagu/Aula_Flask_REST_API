from sql_alchemy import banco

# atributos a ser enviados
class SiteModel(banco.Model):
    # ESCOPO Banco de Dados
    __tablename__ = 'site'
    site_id = banco.Column(banco.Integer, primary_key = True) # id auto incrementado
    url = banco.Column(banco.String(80)) # endereço
    hoteis = banco.relationship('HotelModel', back_populates='site', lazy='dynamic') # Relacionamento reverso
    '''
    relationship: é uma função do SQLAlchemy que é usada para definir uma relação entre duas tabelas.
    back_populates='__tablename__': Este parâmetro é usado para definir a relação bidirecional.
    lazy='dynamic': Este parâmetro define como a carga dos dados relacionados será tratada. (não obrigatório)
    '''

    # ESCOPO Flask
    def __init__(self, url):
        self.url = url

    # método json
    def json(self):
        return {
            'site_id': self.site_id,
            'url': self.url,
            'hoteis': [hotel.json() for hotel in self.hoteis] # Chamada lista hoteis
        }
    
    # método filtro
    @classmethod # recebe a própria como argumento "cls"
    def find_site(cls, url):
        # filtra Banco de dados e retorna 1º resultado
        site = cls.query.filter_by(url=url).first()

        if site:
            return site
        else:
            return False
        
    @classmethod # recebe a própria como argumento "cls"
    def find_by_id(cls, site_id):
        # filtra Banco de dados e retorna 1º resultado
        site = cls.query.filter_by(site_id=site_id).first() # lista de site

        if site:
            return site
        else:
            return False

    # método salvar dados
    def save_site(self):
        banco.session.add(self)
        banco.session.commit()

    # método delete
    def delete_site(self):

        # deletar lista de hoteis associado ao "site_id"
        [hotel.delete_hotel() for hotel in self.hoteis] # "compreensão de lista" ou "list comprehension"
        
        # deletar site
        banco.session.delete(self)
        banco.session.commit()

