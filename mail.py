import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def mailing(mailto, order, file):
    while os.path.exists(file) is False:
        pass
    mail_content = f"""Hi {order[2]},

I hope you’re well! Please see attached invoice number {order[0]} for order created on {order[1]}. Don’t hesitate to reach out if you have any questions.

Kind regards,

AuBasket!"""
    # The mail addresses and password
    sender_address = 'uprevolteam@gmail.com'
    sender_pass = 'MZmX9&jCZK'
    # report_file = open('index.html')
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = mailto
    message['Subject'] = "Thank you for shopping with us!"
    message.attach(MIMEText(mail_content, 'plain'))
    # message.attach(MIMEText(html, 'html'))
    attachment = open(file, "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % file)
    message.attach(p)

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    try:
        text = message.as_string()
        session.sendmail(sender_address, mailto, text)
    except:
        print("Can't Send Mail")
    session.quit()
    print('Mail Sent to: ', order)

