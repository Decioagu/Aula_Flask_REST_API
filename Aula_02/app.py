from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis 

# sintaxe do Flask
app = Flask(__name__)
api = Api(app)

# rota 
api.add_resource(Hoteis, '/hoteis')
# endereço: http://127.0.0.1:5000/hoteis

# execução arquivo principal
if __name__ == '__main__':
    app.run(debug=True)
