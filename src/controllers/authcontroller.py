import json
import jwt
import datetime
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from config import SECRET_KEY, TOKEN_FILE, TOKEN_LIFETIME_SECONDS
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from src.models.dbengine import session_scope

from src.models.user import User
from src.views.authview import AuthView


PH = PasswordHasher()

class AuthController:

    _json_key_name = 'token'
    _token_key_name = 'login'

    def __init__(self):
        self.view = AuthView()

    @classmethod
    def get_login_from_token(cls):
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
    
    def get_authenticated_user(self, session):
        """
        Check user credentials and ask for loggin if token expired or not found
        Returns user instance
        """
        login = self.get_login_from_token()
        while login == None:
            login = self.login()
        return User.get_from_login(session, login)
    

    def login(self):
        with session_scope() as s:
            while True:    
                login = self.view.get_login()
                user = User.get_from_login(session=s, login=login)
                if user:
                    break
                self.view.not_found()
            while True:
                password = self.view.get_password()
                try:
                    PH.verify(user.password, password)
                    break
                except VerifyMismatchError:
                    self.view.bad_password()
            success = self.gen_token(user)
            self.view.success(success)
            return user.login
 
    def verify_auth(self):
        """
        Verify validity of jwt token in json file.
        Returns user login
        """
        login = self.get_login_from_token()
        if login:
            self.view.valid_token(login)
            return login
        else:
            self.view.invalid_token()
