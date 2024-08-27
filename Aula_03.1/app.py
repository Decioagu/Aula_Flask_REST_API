from flask import Flask
from flask_restful import Api
from resources.hotel import Hoteis, Hotel

# sintaxe do Flask
app = Flask(__name__)
api = Api(app)

# rotas
api.add_resource(Hoteis, '/hoteis')
api.add_resource(Hotel, '/hoteis/<string:hotel_id>')

# execução arquivo principal
if __name__ == '__main__':
    app.run(debug=True)

# Seção 6