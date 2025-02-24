from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel
from resources.usuario import Usuario, CadastroUsuario, UsuarioLogin
from config.config_DB import Config
from flask_jwt_extended import JWTManager # autenticação e criptografia

# instanciar Flask
app = Flask(__name__)
app.config.from_object(Config) # configuração do banco
api = Api(app)

# instanciar JWT (JSON Web Token) 
jwt = JWTManager(app)

# executada antes de cada solicitação do aplicativo Flask
@app.before_request 
def cria_banco():
    banco.create_all()

#rota
@app.route('/')
def index():
    return '<h1> Hotel </h1>'

# rotas
api.add_resource(Hoteis, '/hoteis') # acessar cadastro do hoteis 
api.add_resource(Hotel, '/hoteis/<string:hotel_id>') # cadastro do hoteis
api.add_resource(Usuario, '/usuarios/<int:usuario_id>') # cadastro do usuário
api.add_resource(CadastroUsuario, '/cadastro') # cadastrar usuário
api.add_resource(UsuarioLogin, '/login') # acessar cadastro do usuário

# execução arquivo principal
if __name__ == '__main__':
    # instanciar banco
    from config.sql_alchemy import banco
    banco.init_app(app)

    app.run(debug=True) # instanciar api

# Seção 8