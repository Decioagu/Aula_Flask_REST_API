from flask import Flask
from flask_restful import Resource, Api

'''
O Flask é um microframework para desenvolvimento web escrito em Python.  
É conhecido pela sua simplicidade e flexibilidade, possibilitando a 
criação de sites, aplicativos web e APIs de forma rápida e eficiente.
'''

# sintaxe do Flask
app = Flask(__name__)
api = Api(app)

# Ler (recurso da rota)
class Hoteis(Resource):
    def get(self):
        return {'hoteis': 'meus hoteis'}

# rota 
api.add_resource(Hoteis, '/')

# execução arquivo principal
if __name__ == '__main__':
    app.run(debug=True)
