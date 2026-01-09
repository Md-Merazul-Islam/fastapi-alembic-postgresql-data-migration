import random
from datetime import datetime, timedelta

OTP_EXPIRES_IN = 5
OTP_EXPIRATION_TIME = timedelta(minutes=OTP_EXPIRES_IN)
otp_store = {}


def generate_otp(email: str):
    otp_code = str(random.randint(100000, 999999))
    otp_store[email] = {
        "otp": otp_code,
        "expires_at": datetime.now() + OTP_EXPIRATION_TIME,
    }
    return otp_code

def check_otp(email: str, otp: str):
    if email not in otp_store:
        return False
    if otp_store[email]["expires_at"] < datetime.now():
        return False
    return otp_store[email]["otp"] == otp