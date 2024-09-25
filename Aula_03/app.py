from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from config.config_DB import Config 

# sintaxe do Flask
app = Flask(__name__)
app.config.from_object(Config) # configuração do banco
api = Api(app)

# executada antes de cada solicitação do aplicativo Flask
@app.before_request # @app.before_first_request => desuso
def cria_banco():
    banco.create_all()

#rota
@app.route('/')
def index():
    return '<h1> Hotel </h1>'

# rotas
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

# execução arquivo principal
if __name__ == '__main__':
    
    from config.sql_alchemy import banco # ORM (Object-Relational Mapping)
    banco.init_app(app) # instanciar banco

    app.run(debug=True) # instanciar api

# Seção 7