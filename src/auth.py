import sys
sys.path.append("..") # Adds higher directory to python modules path.
from config import SECRET_KEY, TOKEN_FILE, TOKEN_LIFESPAN_MINUTES

import json
import jwt
import datetime

class AuthManager:
    """
    Manager for user authentication
    """
    _json_key_name = 'token'
    _token_key_name = 'email'

    def __init__(self, user):
        self.user = user

    @classmethod
    def auth(cls):
        with open(TOKEN_FILE) as f:
            token = json.load(f)[cls._json_key_name]
            email = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])[cls._token_key_name] 
            return email

    @classmethod
    def gen_token(cls, user):
        email = user.email
        payload = {cls._token_key_name:email, 'exp':datetime.datetime.now() + datetime.timedelta(seconds=30)}
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        file = open(TOKEN_FILE, 'w')
        json.dump({cls._json_key_name:token}, file)
        file.close()
        return True
