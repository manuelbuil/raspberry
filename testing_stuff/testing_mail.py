# Import smtplib for the actual sending function
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

msg = MIMEMultipart()
msg['From'] = 'telecolega@gmail.com'
msg['To'] = 'manuelbuil87@gmail.com'
msg['Subject'] = "SUBJECT OF THE"
body = 'Testing!'

msg.attach(MIMEText(body, 'plain'))


# Send the message via our own SMTP server, but don't include the
# envelope header.
gmail_user = ''
gmail_pwd = ''
s = smtplib.SMTP('smtp.gmail.com',587)
s.starttls()
s.login(gmail_user, gmail_pwd)
text = msg.as_string()
s.sendmail(gmail_user, msg['To'], text)
s.close()
