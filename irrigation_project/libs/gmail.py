import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def create_message(body):
    msg = MIMEMultipart()
    msg['From'] = 'telecolega.raspberry@gmail.com'
    msg['To'] = 'manuelbuil87@gmail.com'
    msg['Subject'] = "Somebody needs water..."
    msg.attach(MIMEText(body, 'plain'))
    return msg

def send_mail(body):

    gmail_user = 'telecolega.raspberry@gmail.com'
    gmail_pwd = 'raspberr'
    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.login(gmail_user, gmail_pwd)
    msg = create_message(body)
    text = msg.as_string()
    try:
        s.sendmail(gmail_user, msg['To'], text)
        s.close()
        return True
    except:
        return False
