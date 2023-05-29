from datetime import datetime
import re
import json
from email.utils import parsedate_tz, mktime_tz
from utils.get_date import get_date
from utils.get_body import get_body

def pago_banco_estado(service, messages, desired_month):
       payments = []
       count = 0
       total_payment = 0
       print('-----------------------------------')
       print("Banco Estado")
       for message in messages:
              msg = service.users().messages().get(userId='me', id=message['id']).execute()
              data = msg['payload']['parts'][1]['body']['data']
              email_body = get_body(data)

              payment_info = re.findall(r'cliente\s*(.*?),\s*con los siguientes datos:\s*Monto transferido:\s*\$(.*?)\n', email_body, re.DOTALL)
              date = get_date(msg['payload']['headers'])  # get the date
              if date is not None and date.month == desired_month and date.year == datetime.now().year :
                     if payment_info:  # Check if payment_info is not empty
                            count += 1
                            name, payment = payment_info[0]
                            formatted_date = date.strftime('%d/%m/%Y') if date is not None else ''
                            payments.append({'name': name, 'payment': payment, 'date': formatted_date})

                            total_payment += float(payment.replace('$', '').replace('.', ''))
                            print(f'{count}. {formatted_date} - {name} - {payment} CLP')
       print(f'Total: {total_payment} CLP en {count} pagos ')
       # Save the payments to a json file
       with open('payments_banco_estado.json', 'w') as f:              
              json.dump(payments, f)
       return {'total': total_payment, 'count': count}
