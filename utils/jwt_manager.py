from jwt import encode, decode

pwd = 'palabra_clave'

def create_token(data, secret=pwd):
  return encode(payload=data, key=secret, algorithm='HS256')

def validate_token(token, secret=pwd):
  return decode(token, secret, algorithms=['HS256'])