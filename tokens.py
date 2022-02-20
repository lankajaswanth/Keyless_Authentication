from itsdangerous import URLSafeTimedSerializer, SignatureExpired,BadTimeSignature
from dotenv import load_dotenv
load_dotenv()
import os


s = URLSafeTimedSerializer(os.getenv("TOKENSECRET_KEY"))

def generate_confirmation_token(email):
    return s.dumps(email, salt=os.getenv("TOKENSECRET_SALT"))

def confirm_token(token, expiration = 300): # 5 minutes = 60*5 = 300
    try:
        email = s.loads(token, salt=os.getenv("TOKENSECRET_SALT"), max_age=expiration)
    except SignatureExpired:
        return "The token has expired"
    except BadTimeSignature:
        return "the token is invalid"
    return email