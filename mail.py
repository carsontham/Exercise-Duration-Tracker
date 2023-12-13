from flask_mail import Mail, Message

from app import app

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'SUSSClassT02Jan2021@gmail.com'
app.config['MAIL_PASSWORD'] = 'SUSSClassT02123!'

mail = Mail(app)

def send_mail(subject, recipient, message):
    assert subject is not None
    assert recipient is not None
    assert message is not None

    msg = Message(subject = subject,
                    sender = 'SUSSClassT02Jan2021@gmail.com',
                    recipients = [recipient])
    
    msg.body = message
    mail.send(msg)