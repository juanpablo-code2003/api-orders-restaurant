import os

from jwt import encode, decode
from dotenv import load_dotenv

load_dotenv()

pwd = os.environ.get('JWT_SECRET_KEY')
if not pwd:
  raise ValueError('JWT_SECRET_KEY environment variable not found')

def create_token(data, secret=pwd):
  return encode(payload=data, key=secret, algorithm='HS256')

def validate_token(token, secret=pwd):
  return decode(token, secret, algorithms=['HS256'])