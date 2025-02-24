from hmac import compare_digest # comparar senha
from flask_jwt_extended import create_access_token, jwt_required
from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel

# Dados pre definidos (Construtor Global)
atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='Campo login obrigatório')
atributos.add_argument('senha', type=str, required=True, help='Campo senha obrigatório')

# rotas (CRUD)

# rota cadastrar usuário (criar)
class CadastroUsuario(Resource):

    def post(self):
        
        # dados = (Construtor Global).(extrair dados)
        dados = atributos.parse_args()
        
        # (ESCOPO Flask).(método login)(Construtor Global)
        if UsuarioModel.filtro_login_do_usuario(dados['login']):
            return {"mensagem": "Login '{}' já existe!!!".format(dados['login'])}, 400
        else: 
            usuario = UsuarioModel(**dados)
            usuario.save_usuario()
            return {f"mensagem": "Usuário criado com sucesso!!!"}, 201 
        
# rota usuário (buscar, excluir)
class Usuario(Resource):    

    # Solicitar (leitura) por "id"
    def get(self, usuario_id):
        # hotel = (ESCOPO Flask).(método filtro (pesquisa por ID))
        usuario = UsuarioModel.filtro_por_id_usuario(usuario_id)

        if usuario:
            # (ESCOPO Flask).(método json)
            return usuario.json()   
        else:
            return {'mensagem': 'Usuário não existe.'}, 400     

    # Excluir
    @jwt_required() # necessário token de acesso
    def delete(self, usuario_id):

        # hotel = (ESCOPO Flask).(método filtro (pesquisa por ID)) 
        usuario = UsuarioModel.filtro_por_id_usuario(usuario_id) # retorna alguma coisa ou falso

        # Se ID existir
        if usuario:
            # (ESCOPO Flask).(método delete)
            usuario.delete_usuario()
            return {'mensagem': 'Usuário deletado.'}, 200   
        else:
            return {'mensagem': 'Usuário não existe.'}, 400     
        
# rota login usuario (criar senha "Token")
class UsuarioLogin(Resource):

    @classmethod
    def post(cls):
        # dados = (Construtor Global).(extrair dados)
        dados = atributos.parse_args()

        print('===================>',dados)

        # (ESCOPO Flask).(método login)(Construtor Global)
        usuario = UsuarioModel.filtro_login_do_usuario(dados['login'])

        #  compare_digest() => realizar comparações seguras de strings
        if usuario and compare_digest(usuario.senha, dados['senha']):
            # create_access_token() => usado em sistema de autenticação e autorização
            token_de_acesso = create_access_token(identity=str(usuario.usuario_id))
            '''OBS: "identity" dentro do token JWT deve ser uma string'''

            return {'token de acesso': token_de_acesso}, 200
        return {'mensagem': 'Usuário ou senha errado.'}, 400 # Unauthorized
