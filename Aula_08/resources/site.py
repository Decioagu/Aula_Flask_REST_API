from flask_restful import Resource
from models.site import SiteModel 
from flask_jwt_extended import jwt_required

# rota visualizar Sites
class Sites(Resource):
    # método de (Leitura)
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}

# rota CRUD
class Site(Resource):
    # Solicitar (leitura) por "url"
    def get(self, url):
        # site = (ESCOPO Flask).(método filtro (pesquisa por "url"))
        site = SiteModel.filtro_por_id_URL(url)
        if site:
            # (ESCOPO Flask).(método json)
            return site.json()
        else:
            return {'mensagem': 'Site não existe'}, 400
        
    # Enviar (criar)
    @jwt_required() # necessário token de acesso
    def post(self, url):
        # site = (ESCOPO Flask).(método filtro (pesquisa por "url"))
        site = SiteModel.filtro_por_id_URL(url)
        if site:
            return {'mensagem': 'Site já existe'}, 400
        else:
            # acesso ao banco de dados com "url"
            novo_site = SiteModel(url)
            try:
                # (ESCOPO Flask).(método salvar dados)
                novo_site.save_site()
                return novo_site.json()
            except:
                return {'mensagem': 'Ocorreu um erro interno'}, 500

    # Excluir
    @jwt_required() # necessário token de acesso
    def delete(self, url):
        # site = (ESCOPO Flask).(método filtro (pesquisa por "url"))
        site = SiteModel.filtro_por_id_URL(url)
        if site:
            try:
                # deletar site
                site.delete_site()
                return {'mensagem': 'Site deletado'}, 200
            except:
                return {'mensagem': 'Ocorreu um erro interno ao deletar o site'}, 500
        else:
            return {'mensagem': 'Site não existe'}, 400