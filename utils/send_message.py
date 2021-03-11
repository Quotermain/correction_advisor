import smtplib, ssl
from email.mime.text import MIMEText
from sys import argv

PORT = 465
LOGIN = 'pavelhat233@gmail.com'
PASSWORD = 'quotermain233'

def send_message(message):
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=context) as server:
		server.login(LOGIN, PASSWORD)
		sender = LOGIN
		reciever = 'bpconsult45@gmail.com'

		msg = MIMEText(message)
		msg['Subject'] = message
		msg['To'] = reciever
		msg['From'] = sender

		server.sendmail(sender, reciever, msg.as_string())

if __name__ == '__main__':
	message = argv[1]
	send_message(message)
