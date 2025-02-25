from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt ###
import datetime

# Criação do aplicativo Flask
app = Flask(__name__)

# Chave secreta para assinar o JWT
app.config["JWT_SECRET_KEY"] = "DontTellAnyone"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(minutes=10)  # Token expira após 10 minutos

jwt = JWTManager(app)

# Blacklist de tokens
BLACKLIST = set() ###

# Rota de login (para gerar o token)
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    password = request.json.get("password")

    # Aqui você faria a verificação do usuário e senha (ex: banco de dados)
    if username == "admin" and password == "admin":
        # Criação do token JWT
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200

    return jsonify({"msg": "Credenciais inválidas"}), 401

# Rota protegida (requer o token JWT)
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

### --------------------------- BLACKLIST ----------------------------
# Rota para revogar o token (adicionar à blacklist)
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # Pega identificação do usuário e o próprio token    
    BLACKLIST.add(jti) # adicionar token na lista de invalido apos "saída de login" 
    return jsonify({"msg": "Você foi desconectado com sucesso!"}), 200

# Função verifica se o token está na lista de bloqueados
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):  # checagem de token na lista BLACKLIST
    return jwt_payload['jti'] in BLACKLIST # jwt_payload é um dicionário com os tokens
### ------------------------------------------------------------------

if __name__ == '__main__':
    app.run(debug=True)
