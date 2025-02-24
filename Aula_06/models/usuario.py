from config.sql_alchemy import banco

# atributos a ser enviados
class UsuarioModel(banco.Model):
    # ESCOPO Banco de Dados (cls)
    __tablename__ = 'usuarios'
    usuario_id = banco.Column(banco.Integer, primary_key = True, autoincrement=True) # id auto incremento
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))
    '''banco.Model é equivalente a declarative_base() do SQLAlchemy'''

    # ESCOPO Flask (Construtor)
    def __init__(self, login, senha):
        self.login = login
        self.senha = senha
       
    # método json (resposta usuário)
    def json(self):
        return {
            'usuario_id': self.usuario_id,
            'login': self.login
        }
    
    # método filtro
    @classmethod # recebe a própria como argumento "cls"
    def filtro_por_id_usuario(cls, usuario_id):

        # filtra Banco de dados e retorna 1º resultado
        usuario = cls.query.filter_by(usuario_id=usuario_id).first()

        if usuario:
            return usuario
        else:
            return False

    # método salvar dados
    def save_usuario(self):
        banco.session.add(self)
        banco.session.commit()

    # método delete
    def delete_usuario(self):
        banco.session.delete(self)
        banco.session.commit()

    # método login
    @classmethod # recebe a própria como argumento "cls"
    def filtro_login_do_usuario(cls, login):
        # filtra Banco de dados e retorna 1º resultado
        usuario = cls.query.filter_by(login=login).first()

        if usuario:
            return usuario
        else:
            return False

