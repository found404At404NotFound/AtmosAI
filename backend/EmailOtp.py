import smtplib as smt
from email.mime.text import MIMEText as mt
import random as rd
import os
from dotenv import load_dotenv

load_dotenv()

class EmailNotValid(Exception):
    pass

def sendOTP(email):
    otp = rd.randint(10000, 99999)
    try:
        # Fetch sender email and password from .env
        sender = os.getenv('EMAIL_ADDRESS')
        password = os.getenv('EMAIL_PASSWORD')

        if not sender or not password:
            raise EmailNotValid("Email sender or password not set in environment variables")

        msg = mt(f'Your OTP is : {otp}\n\nKindly Do not reply to this email.')
        msg["From"] = sender
        msg["To"] = email
        msg["Reply-To"] = "noreply@example.com"

        with smt.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, email, msg.as_string())

        print(f"OTP sent to {email}: {otp}")

    except Exception as e:
        print("Email sending failed:", e)

    # Always return OTP (whether mail sent or not)
    return otp