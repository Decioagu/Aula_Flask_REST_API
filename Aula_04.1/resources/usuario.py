from hmac import compare_digest # comparar senha
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restful import Resource, reqparse
from config.blacklist import BLACKLIST
from models.usuario import UsuarioModel

# Dados pre definidos (Construtor Global)
atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='Campo login obrigatório')
atributos.add_argument('senha', type=str, required=True, help='Campo senha obrigatório')

# rota (CRUD)
class Usuario(Resource):    

    # Solicitar (leitura) por "id"
    def get(self, usuario_id):
        # hotel = (ESCOPO Flask).(método filtro (pesquisa por ID))
        usuario = UsuarioModel.find_usuario(usuario_id)

        if usuario:
            # (ESCOPO Flask).(método json)
            return usuario.json()   
        else:
            return {'mensagem': 'Usuário não existe.'}, 404           

    # Excluir
    @jwt_required() # necessário token de acesso
    def delete(self, usuario_id):

        # hotel = (ESCOPO Flask).(método filtro (pesquisa por ID)) 
        usuario = UsuarioModel.find_usuario(usuario_id) # retorna alguma coisa ou falso

        # Se ID existir
        if usuario:
            # (ESCOPO Flask).(método delete)
            usuario.delete_usuario()
            return {'mensagem': 'Usuário deletado.'}, 200   
        else:
            return {'mensagem': 'Usuário não existe.'}, 404
        
# rota cadastrar usuário
class CadastroUsuario(Resource):

    def post(self):
        
        # dados = (Construtor Global).(extrair dados)
        dados = atributos.parse_args()
        
        # (ESCOPO Flask).(método login)(Construtor Global)
        if UsuarioModel.find_by_login(dados['login']):
            return {"mensagem": "Login '{}' já existe!!!".format(dados['login'])}, 200
        else: 
            usuario = UsuarioModel(**dados)
            usuario.save_usuario()
            return {f"mensagem": "Usuário criado com sucesso!!!"}, 201

# rota login
class UsuarioLogin(Resource):

    @classmethod
    def post(cls):
        # dados = (Construtor Global).(extrair dados)
        dados = atributos.parse_args()

        # (ESCOPO Flask).(método login)(Construtor Global)
        usuario = UsuarioModel.find_by_login(dados['login'])

        #  compare_digest() => realizar comparações seguras de strings
        if usuario and compare_digest(usuario.senha, dados['senha']):
            # create_access_token() => usado em sistema de autenticação e autorização
            token_de_acesso = create_access_token(identity=usuario.usuario_id)
            return {'acesso token': token_de_acesso}, 200
        return {'mensagem': 'Usuário ou senha errado.'}, 401 # Unauthorized

# rota logout
class UsuarioLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id) # lista de token invalido apos "saída de login" 
        return {'mensagem' : 'Saiu do login com sucesso!!!'}, 200