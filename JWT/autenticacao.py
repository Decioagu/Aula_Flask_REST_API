from flask import Flask, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import os

app = Flask(__name__)

# Configuração da chave secreta para assinar os tokens
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_secret")
jwt = JWTManager(app)

# Rota de login que gera um token JWT
@app.route("/login", methods=["POST"])
def login():
    id = 1
    # OBS: o "identity" dentro do token JWT deve ser uma string
    token_de_acesso = create_access_token(identity= str(id))
    '''
    Se identity= 1, número inteiro, pode ocorrer o erro:
        {
            "msg": "Subject must be a string"
        }
    '''
    # jsonify → Converte dicionários Python para respostas JSON formatadas.
    return jsonify(token_de_acesso=token_de_acesso)

# Rota protegida que exige um token JWT válido
@app.route("/protegido", methods=["GET"])

@jwt_required()
def protegido():
    usuario = get_jwt_identity()  # Obtém o usuário do token
    
    # jsonify → Converte dicionários Python para respostas JSON formatadas.
    return jsonify(msg=f"Bem-vindo, {usuario}!")

if __name__ == "__main__":
    app.run(debug=True)
