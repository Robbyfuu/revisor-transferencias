from datetime import datetime
import re
import json
from email.utils import parsedate_tz, mktime_tz
from utils.get_date import get_date
from utils.get_body import get_body

def pago_banco_scotia(service, messages, desired_month):
       payments = []
       count = 0
       total_payment = 0
       print('-----------------------------------')
       print("Banco Scotia")
       for message in messages:
              msg = service.users().messages().get(userId='me', id=message['id']).execute()
              data = msg['payload']['parts'][0]['parts'][0]['body']['data']
              email_body = get_body(data)
              date = get_date(msg['payload']['headers'])  # get the date

              if date is not None and date.month == desired_month and date.year == datetime.now().year:
                match = re.search(r'Sr\(a\) (.*?) ha instruido', email_body)
                if match:
                    sender_name = match.group(1)
                else:
                    sender_name = None

                match =  re.search(r"Monto\s*:\s*([\d\.]+)", email_body, re.MULTILINE)

                if match:
                    payment = match.group(1)
                else:
                    payment = None 

                count += 1
                name = sender_name
                formatted_date = date.strftime('%d/%m/%Y') if date is not None else ''
                payments.append({'name': name, 'payment': payment, 'date': formatted_date})
                if payment is not None:
                    total_payment += float(payment.replace('$', '').replace('.', ''))
                print(f'{count}. {formatted_date} - {name} - {payment} CLP')
       print(f'Total: {total_payment} CLP en {count} pagos ')
       # Save the payments to a json file
       print('-----------------------------------')
       with open('payments_banco_estado.json', 'w') as f:              
              json.dump(payments, f)
       return {'total': total_payment, 'count': count}