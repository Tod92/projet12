import click
from src.views.view import View


class AuthView(View):

    def get_login(self):
        return click.prompt('Please enter login', type=str)

    def not_found(self):
        click.echo("USER NOT FOUND !!")

    def success(self, bool=True):
        if bool == True:
            click.echo("Authentication OK !")
        else:
            click.echo("SOMETHING WENT WRONG !!")

    def bad_password(self):
        click.echo("INCORRECT PASSWORD !!")

    def valid_token(self, login):
        click.echo(f"Valid token found for user {login}")

    def invalid_token(self):
        click.echo(f"Token invalid or not present !")

