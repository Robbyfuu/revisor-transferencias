import requests
import json
def valor_dolar():
    url = "https://mindicador.cl/api/dolar/"
    response = requests.get(url)
    data = response.json()

    primer_valor = data['serie'][0]['valor']
    return primer_valor