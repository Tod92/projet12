
import click
from src.views.view import View


class UserView(View):
    
    def detail(self, user):
        click.echo(f'{user.id}:{user.fullName} login:{user.login} email:{user.email} role:{user.role.name}')

    def get_info(self):
        firstName = self.get_str('Please enter first name', max_length=50)
        lastName = self.get_str('Please enter last name', max_length=50)
        login = self.get_str('Please enter login', max_length=4)
        email = self.get_str('Please enter email', max_length=50)
        password = self.get_password()
        return firstName, lastName, login, email, password
 
    def get_login(self):
        return click.prompt('Please enter login', type=str)
        
    def not_found(self):
        click.echo("USER NOT FOUND !!")
 
    def bad_password(self):
        click.echo("INCORRECT PASSWORD !!")
    
    def success(self, bool=True):
        if bool == True:
            click.echo("Authentication OK !")
        else:
            click.echo("SOMETHING WENT WRONG !!")

    def valid_token(self, login):
        click.echo(f"Valid token [{login}] found in local files")

    def invalid_token(self):
        click.echo(f"Token found in local files but not valid !")

    def is_logged_in(self, name):
        click.echo(f"You are logged in as {name}")
   