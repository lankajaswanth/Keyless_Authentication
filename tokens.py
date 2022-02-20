from itsdangerous import URLSafeTimedSerializer, SignatureExpired,BadTimeSignature
from dotenv import load_dotenv
load_dotenv()
import os


s = URLSafeTimedSerializer(os.getenv("TOKENSECRET_KEY"))

def generate_confirmation_token(email):
    return s.dumps(email, salt=os.getenv("TOKENSECRET_SALT"))