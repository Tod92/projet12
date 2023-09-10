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
        click.echo("USER NOT FOUND !!")
 
    def bad_password(self):
        click.echo("INCORRECT PASSWORD !!")
    
    def success(self, bool=True):
        if bool == True:
            click.echo("Authentication OK !")
        else:
            click.echo("SOMETHING WENT WRONG !!")

    def valid_token(self):
        click.echo("Valid token found in local files")

    def invalid_token(self):
        click.echo("Token found but not valid !")

    def is_logged_in(self, name):
        click.echo(f"You are logged in as {name}")

class ClientView(View):
    def detail(self, client):
        click.echo(f'{client.id}:{client.firstName} {client.lastName} {client.email} phone:{client.phone} company:{client.company.name} ' +\
                   f'created:{client.creationDate} last update:{client.lastUpdateDate}')

class ContractView(View):
    def detail(self, contract):
        click.echo(f'{contract.id}:{contract.status.name} {contract.client.firstName} {contract.client.lastName} ({contract.client.company.name}) '+\
                   f'amount :{contract.totalAmount} pending:{contract.remainingAmount} commercial:{contract.commercialContact.login} created:{contract.creationDate}')
        
class EventView(View):
    def detail(self, event):
        click.echo(f'{event.id}: {event.name} ({event.contract.client.company.name}) debut:{event.startDate} fin:{event.endDate} ' +\
                   f'attendees:{event.attendees} location:{event.location.address}')

class LocationView(View):
    """"""

    def run(self):
        self.address = click.prompt('Please enter location address', type=str)
        return self.address