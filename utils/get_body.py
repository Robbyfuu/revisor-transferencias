import base64
from bs4 import BeautifulSoup



def decode_base64(data):
    """Decodificar base64, rellenado si es necesario"""
    missing_padding = len(data) % 4
    if missing_padding != 0:
        data += b'='* (4 - missing_padding)
    return base64.urlsafe_b64decode(data)

def get_body(message):
    """Esta función extrae el cuerpo del correo electrónico y lo devuelve como un texto limpio."""
    decoded_data = decode_base64(message)
    soup = BeautifulSoup(decoded_data, 'html.parser')
    return soup.get_text()