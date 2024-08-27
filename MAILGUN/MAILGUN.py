import os
import requests
from dotenv import load_dotenv 

load_dotenv()
MAILGUN_DOMAIN = os.getenv('DOMINIO')
MAILGUN_API_KEY = os.getenv('CHAVE')
FROM_TITLE = os.getenv('TITULO')
FROM_EMAIL = os.getenv('ENVIO')
MEU_EMAIL = os.getenv('EMAIL')

# https://login.mailgun.com/login/
def envio_de_email():
        
        return requests.post(f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages',
                    auth=('api', MAILGUN_API_KEY),
                    data={'from': f'{FROM_TITLE} <{FROM_EMAIL}>',
                        'to': MEU_EMAIL,
                        'subject': 'Confirmação de Cadastro.',
                        'html': f'<html><p>Seu cadastro foi confirmado.</p></html>'
                        }
                        )

envio_de_email()
print("\nEnviado\n")