import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
from .models import User

def resetpwdlink(item):
    email_id = 'stefenwarner13@gmail.com'
    email_pass = 'iyutbwcpmhehhmuc'
    msg = EmailMessage()    
    msg['Subject'] = 'Reset password link'
    msg['From'] = email_id
    msg['To'] = item[0].email
    identify = item[0].email
    token = generate_token()  
    msg.set_content(f"http://127.0.0.1:8000/api/RestPassword/{token}/{identify}/")   
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as mail:
        mail.login(email_id, email_pass)
        mail.send_message(msg)  

def send_activation_link(serialized_data):
    email_id = 'stefenwarner13@gmail.com'
    email_pass = 'iyutbwcpmhehhmuc'
    msg = EmailMessage()    
    msg['Subject'] = 'Account Activation link'
    msg['From'] = email_id
    msg['To'] = serialized_data["email"]
    identify = serialized_data["email"]
    token = generate_token()  
    url = f"http://127.0.0.1:8000/api/activation/{token}/{identify}/"
    msg.set_content(url)
    item = User.objects.get(phone_number = serialized_data["phone_number"])
    item.activation_link = url 
    item.save()
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as mail:
        mail.login(email_id, email_pass)
        mail.send_message(msg)

def generate_token():
    otp = ''
    num = "1234567890"
    for i in range(4):
        otp += random.choice(num)
    return otp        