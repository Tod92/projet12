import sys
sys.path.append("..") # Adds higher directory to python modules path.
from config import SECRET_KEY, TOKEN_FILE, TOKEN_LIFETIME_SECONDS

import json
import jwt
import datetime

class AuthManager:
    """
    Manager for user authentication
    """
    _json_key_name = 'token'
    _token_key_name = 'login'

    def __init__(self, user):
        self.user = user

    @classmethod
    def auth(cls):
        with open(TOKEN_FILE) as f:
            token = json.load(f)[cls._json_key_name]
            try:
                result = jwt.decode(token, SECRET_KEY, algorithms="HS256")
                return result[cls._token_key_name]
            except jwt.ExpiredSignatureError:
                return None



    @classmethod
    def gen_token(cls, user):
        """
        Creates a jwt token with wanted lifetime, with payload : {"login":"userlogin"}
        saves it in local json file 
        """
        login = user.login
        payload = {cls._token_key_name:login, 'exp':datetime.datetime.now(tz=datetime.timezone.utc)\
                    + datetime.timedelta(seconds=TOKEN_LIFETIME_SECONDS)}
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        file = open(TOKEN_FILE, 'w')
        json.dump({cls._json_key_name:token}, file)
        file.close()
        return True
