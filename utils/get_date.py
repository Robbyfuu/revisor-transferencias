from datetime import datetime
from email.utils import parsedate_tz, mktime_tz
def get_date(headers):
    for d in headers:
        if d['name'] == 'Date':
            timestamp = mktime_tz(parsedate_tz(d['value']))
            return datetime.fromtimestamp(timestamp)
    return None
def today():
    return datetime.now().strftime('%d-%m-%Y')