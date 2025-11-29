import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import dns.resolver
def send_verification_code(to_email):
    code = str(random.randint(100000, 999999))
    sender_email = "managewallet8@gmail.com"
    sender_password = "xkju cxsx apgv nwpp"  
    subject = "کد تایید شما"
    body = f"کد تایید شما: {code}"
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return code  
    except:
        return False
    
def is_valid_email(email_address):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern,email_address) is not None:
        domain = email_address.split("@")[1]
        try:
            dns.resolver.resolve(domain, 'MX')
            return True
        except:
            return False
    else:
        return False