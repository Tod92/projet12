import json
import jwt
import datetime

from sqlalchemy import select
import sys
sys.path.append("..") # Adds higher directory to python modules path.
from config import SECRET_KEY, TOKEN_FILE, TOKEN_LIFETIME_SECONDS

from src.models.dbengine import session_scope
from src.controllers.permissions import PermissionsMixin
from src.models.user import User
from src.views.userview import UserView
from src.models.role import Role



class UserController(PermissionsMixin):
    """
    """
    _table_name = 'user'

    _list_permissions = ['isAuth']
    _create_permissions = ['isGestion']
    _update_permissions = ['isGestion']
    _updatables = ['firstName', 'lastName', 'email', 'login', 'password', 'role']

    def __init__(self):
        self.view = UserView()    

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
        login = AuthManager.check_token()
        if login:
            self.view.valid_token(login)
            return login
        else:
            self.view.invalid_token()

    def list(self, option=None):
        self._permissions = self._list_permissions
        with session_scope() as s:
            self.has_permission(s)
            users = User.get_all(s)
            self.view.list_instances(users)

    def create(self, option=None):
        self._permissions = self._create_permissions
        with session_scope() as s:
            self.has_permission(s)
            self.view.creation_starting(self._table_name)
            user = User()
            # Prompting role for user
            roles = Role.get_all(s)
            user.role_id = self.view.list_instances(roles, prompt=True)
            # Prompting user informations
            user.firstName = self.view.get_str('First Name', max_length=50)
            user.lastName = self.view.get_str('Last Name', max_length=50) 
            user.login = self.view.get_str('Login', max_length=4)
            user.email  = self.view.get_str('Email', max_length=50)
            user.set_password(self.view.get_str('Password', max_length=15))
            # Creating entry
            s.add(user)

    def update(self, option=None):
        with session_scope() as s:
            # First permission check for list
            self._permissions = self._list_permissions
            self.has_permission(s)
            users = User.get_all(s)
            choice = self.view.list_instances(users, prompt=True)
            self.instance = users[choice-1]
            # Second permission check for update
            self._permissions = self._update_permissions
            self.has_permission(s)
            choice = self._updatables[self.view.pick_in_attr(self._updatables, self.instance)]
            if choice == 'firstName':
                self.instance.firstName = self.view.get_str('First Name', max_length=50)
            elif choice == 'lastName':
                self.instance.lastName = self.view.get_str('Last Name', max_length=50)
            elif choice == 'email':
                self.instance.email = self.view.get_str('Email', max_length=50)
            elif choice == 'login':
                self.instance.login = self.view.get_str('Login', max_length=4)
            elif choice == 'role':
                roles = Role.get_all(s)
                self.instance.role_id = self.view.list_instances(roles, prompt=True)
            elif choice == 'password':
                self.instance.set_password(self.view.get_str('Password', max_length=15))




