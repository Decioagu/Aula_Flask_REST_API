from hmac import compare_digest # comparar senha
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.usuario import UsuarioModel
import traceback
from flask import make_response, render_template

# Dados pre definidos (Construtor Global)
atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help='Campo login obrigatório')
atributos.add_argument('senha', type=str, required=True, help='Campo senha obrigatório')
atributos.add_argument('email', type=str) ###
atributos.add_argument('ativado', type=bool) ###

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

        ### (Construtor Global). email
        if not dados.get('email') or dados.get('email') is None:
            return {'mensagem': 'email não pode ser deixado em branco.'}, 400
        
        ### (ESCOPO Flask).(método email)(Construtor Global)
        if UsuarioModel.find_by_email(dados['email']):
            return {"mensagem": "E-mail '{}' já existe!!!".format(dados['email'])}, 400

        # (ESCOPO Flask).(método login)(Construtor Global)
        if UsuarioModel.find_by_login(dados['login']):
            return {"mensagem": "Login '{}' já existe!!!".format(dados['login'])}, 400
        else: 
            usuario = UsuarioModel(**dados)
            usuario.ativado = False ###
            try:
                usuario.save_usuario()
                usuario.envio_de_email()
            except:
                usuario.delete_usuario()
                '''
                traceback.print_exc() é uma função em Python usada para 
                imprimir informações detalhadas sobre uma exceção.
                '''
                traceback.print_exc()
                return {'mensagem': 'Ocorreu erro interno no servidor.'}, 500
            return {f"mensagem": "Usuário criado com sucesso!!!"}, 201

# rota login
class UsuarioLogin(Resource):

    @classmethod
    def post(cls):
        # dados = (Construtor Global).(extrair dados)
        dados = atributos.parse_args()
        # print(dados)
        
        # (ESCOPO Flask).(método login)(Construtor Global)
        usuario = UsuarioModel.find_by_login(dados['login'])
        # print(usuario.json())
        

        #  compare_digest() => realizar comparações seguras de strings
        if usuario and compare_digest(usuario.senha, dados['senha']):

            if usuario.ativado: ###
                # create_access_token() => usado em sistema de autenticação e autorização
                token_de_acesso = create_access_token(identity=usuario.usuario_id)
                return {'acesso token': token_de_acesso}, 200
            else:
                return {'mensagem': 'Usuário não ativo.'}, 400
        return {'mensagem': 'Usuário ou senha errado.'}, 401 # Unauthorized

# rota logout
class UsuarioLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti']
        BLACKLIST.add(jwt_id) # lista de token invalido apos "saída de login" 
        return {'mensagem' : 'Saiu do login com sucesso!!!'}, 200
    
### rota ativação de cadastro
class UsuarioAtivacao(Resource):
    @ classmethod
    def get(cls, usuario_id):
        usuario = UsuarioModel.find_usuario(usuario_id)
        # print(usuario.json())
        
        if not usuario:
            return{'mensagem': 'Usuário com id:{} não foi encontrado'.format(usuario_id)}, 404
        
        usuario.ativado = True
        try:
            usuario.save_usuario()
        except:
            '''
                traceback.print_exc() é uma função em Python usada para 
                imprimir informações detalhadas sobre uma exceção.
            '''
            traceback.print_exc()
            return {'mensagem': 'Ocorreu erro interno no servidor.'}, 500
        
        # # resposta da requisição como JSON
        # return {'mensagem': f'Usuário: ({usuario.login}) de email: ({usuario.email}) encontrado com sucesso!'}, 200
        
        # "headers" indica que a resposta da requisição é uma página HTML e não JSON ou texto.
        headers = {'Content-Type': 'text/html'}

        # make_response(...): Esta função cria uma resposta HTTP personalizada.
        # render_template: Esta função renderiza um template HTML
        return make_response(render_template('user_confirm.html', email=usuario.email, usuario=usuario.login), 200, headers)
    '''
        OBS: o arquivo "user_confirm.html" obrigatoriamente deve ser alocado 
        em uma pasta de nome "templastes", pois o Flask irá procurar este 
        arquivo no diretório de templates da aplicação por padrão.
    ''' 