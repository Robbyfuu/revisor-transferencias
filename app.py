from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from paypal.paypal import pago_paypal
from banco_estado.banco_estado import pago_banco_estado
from scotiabank.scotiabank import pago_banco_scotia
from banco_falabella.falabella import pago_banco_falabella
from utils.get_date import today
from utils.valor_dolar import valor_dolar

# Si modificas estos SCOPES, elimina el archivo token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']



def main():
    """Muestra información básica sobre los mensajes de la bandeja de entrada de un usuario que coinciden con una consulta de búsqueda"""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    results_paypal = service.users().messages().list(userId='me', q='from:paypal subject:"ha recibido un pago"').execute()
    results_banco_estado = service.users().messages().list(userId='me', q='from:BancoEstado subject:"Aviso de envío o recepción de dinero"').execute()
    results_banco_scotia = service.users().messages().list(userId='me', q='from:Notificación Scotia. subject:"Aviso de Transferencia"').execute()
    results_banco_falabella = service.users().messages().list(userId='me', q='from:notificaciones@cl.bancofalabella.com subject:"Aviso de transferencia de fondos recibida"').execute()
    messages_paypal = results_paypal.get('messages', [])
    messages_banco_estado = results_banco_estado.get('messages', [])
    messages_banco_scotia = results_banco_scotia.get('messages', [])
    messages_banco_falabella = results_banco_falabella.get('messages', [])
    monto_total = 0
    pagos = []

    if not messages_paypal:
        print('No se encontraron mensajes de correo electrónico.')
    else:
        print('Pagos:')
        desired_month = int(input('Por favor, introduce el número del mes (1-12) del que deseas información: '))
        monto_paypal = pago_paypal(service, messages_paypal, desired_month)
        monto_banco_estado = pago_banco_estado(service, messages_banco_estado, desired_month)
        monto_banco_scotia = pago_banco_scotia(service, messages_banco_scotia, desired_month)
        monto_banco_falabella = pago_banco_falabella(service, messages_banco_falabella, desired_month)
        monto_total = monto_paypal['total'] *valor_dolar() + monto_banco_estado['total']  + monto_banco_scotia['total']  + monto_banco_falabella['total']
        total_transacciones = monto_paypal['count'] + monto_banco_estado['count'] + monto_banco_scotia['count'] + monto_banco_falabella['count']
        print(f'El monto total es: {monto_total} CLP en {total_transacciones} transacciones')
        pagos.append(monto_banco_estado)
        pagos.append(monto_banco_scotia)
        pagos.append(monto_banco_falabella)
        pagos.append(monto_paypal)
        pagos.append({'total': monto_total, 'count': total_transacciones})
        with open(f'pagos_{today()}.txt', 'w') as f:
            f.write(f'{pagos}')
        print(f'Archivo pagos_{today()}.txt creado con éxito')
    
if __name__ == '__main__':
    main()
