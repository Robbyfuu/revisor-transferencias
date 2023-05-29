from datetime import datetime
import re
import json
from email.utils import parsedate_tz, mktime_tz
from utils.get_date import get_date

def pago_paypal(service, messages, desired_month):
       payments = []
       count = 0
       total_payment = 0
       print('-----------------------------------')
       print("Paypal")
       for message in messages:
              msg = service.users().messages().get(userId='me', id=message['id']).execute()
              # Extract the payment and name from snippet
              payment_info = re.findall(r'Hola, (.*?): (.*?) le ha enviado (.*?) USD', msg['snippet'])
              date = get_date(msg['payload']['headers'])  # get the date
              if date is not None and date.month == desired_month and date.year == datetime.now().year :
                     count += 1
                     name, sender, payment = payment_info[0]
                     formatted_date = date.strftime('%d/%m/%Y') if date is not None else ''
                     payments.append({'name': sender, 'payment': payment, 'date': formatted_date})
                     total_payment += float(payment.replace('$', '').replace(',', '.'))
                     print(f'{count}. {formatted_date} - {sender} - {payment} USD')
       print(f'Total: {total_payment} USD en {count} pagos ')
       print('-----------------------------------')
       # Save the payments to a json file
       with open('payments_paypal.json', 'w') as f:              
              json.dump(payments, f)
       return {'total': total_payment, 'count': count}

