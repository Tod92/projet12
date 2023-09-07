import click






class View:
    pass

class AuthView(View):
    """"""

    def get_login(self):
        self.login = click.prompt('Please enter login', type=str)
        return self.login

    def get_password(self):
        self.password = click.prompt('Please enter password', type=str)
        return self.password
        
    def not_found(self):
        click.echo("USERNAME NOT FOUND !!")
 
    def bad_password(self):
        click.echo("INCORRECT PASSWORD !!")


class LocationView(View):
    """"""

    def run(self):
        self.address = click.prompt('Please enter location address', type=str)
        return self.address