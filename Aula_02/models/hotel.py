# modelo: gerenciamento e validação de dados
class HotelModel:
    # ESCOPO Flask (Construtor)
    def __init__(self, hotel_id, nome, estrelas, diaria, cidade) -> None:
        self.hotel_id = hotel_id # id str via Hesders
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    # método json ( .resources\hotel.py = GET)
    def json(self):
        return {
            'hotel_id' : self.hotel_id,
            'nome' : self.nome,
            'estrelas' : self.estrelas,
            'diaria' : self.diaria,
            'cidade' : self.cidade
        }

# ESCOPO Flask: é modelo de dados permitido para consulta, armazenamento e atualização de dados.   