import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders
import os
from datetime import date, timedelta

yesterday = date.today() - timedelta(days=1)
datecsv = yesterday.strftime('%m_%d_%Y')
print(datecsv)

SUBJECT = '{}'.format(datecsv+"_IgniteEvents")
FILENAME = 'attachthisfile.csv'
FILEPATH = './attachthisfile.csv'
MY_EMAIL = 'administrator@vtion.in'
MY_PASSWORD = 'VTION@2019'
# TO_EMAIL = ['deepa.prajapati@qsstechnosoft.com','manoj.dawane@vtion.in','rajshree.dave@vtion.in','shashank.mehta@vtion.in','process@vtion.in','dhananjai.chitranshi@qsstechnosoft.com','shailesh.varudkar@vtion.in','kamal.thakur@qsstechnosoft.com']
TO_EMAIL = ['kamal.thakur@qsstechnosoft.com']
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

msg = MIMEMultipart()
msg['From'] = MY_EMAIL
msg['To'] = COMMASPACE.join(TO_EMAIL)
msg['Subject'] = SUBJECT


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)

pathtofile = BASE_DIR + str("/target/Data_"+yesterday.strftime('%m_%d_%Y')+'.csv')
FILENAME = str("Data_"+yesterday.strftime('%m_%d_%Y')+'.csv')

part = MIMEBase('application', "octet-stream")
part.set_payload(open(pathtofile, "rb").read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename=FILENAME)  # or
# part.add_header('Content-Disposition', 'attachment; filename="attachthisfile.csv"')
msg.attach(part)

smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(MY_EMAIL, MY_PASSWORD)
smtpObj.sendmail(MY_EMAIL, TO_EMAIL, msg.as_string())
smtpObj.quit()
