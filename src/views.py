import click






class View:
    def permission_denied(self):
         click.echo("PERMISSION DENIED !!")
       

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

class UserView(View):
    def get_info(self):
        firstName = click.prompt('Please enter first name', type=str)
        lastName = click.prompt('Please enter last name', type=str)
        login = click.prompt('Please enter login', type=str)
        email = click.prompt('Please enter email', type=str)
        password = click.prompt('Please enter password', type=str)
        return firstName, lastName, login, email, password
    
    def pick_role(self, roles):
        for r in roles:
            click.echo(f'{r.id} : {r.name}')
        role_id = click.prompt('Please pick a role', type=int)
        return role_id
    

class ClientView(View):
    def detail(self, client):
        click.echo(f'{client.id}:{client.firstName} {client.lastName} {client.email} phone:{client.phone} company:{client.company.name} ' +\
                   f'created:{client.creationDate} last update:{client.lastUpdateDate}')

class ContractView(View):
    def detail(self, contract):
        commercial = 'Empty'
        if contract.commercialContact:
            commercial = contract.commercialContact.login
        click.echo(f'{contract.id}:{contract.status.name} {contract.client.firstName} {contract.client.lastName} ({contract.client.company.name}) '+\
                   f'amount :{contract.totalAmount} pending:{contract.remainingAmount} commercial:{commercial} created:{contract.creationDate}')

    def get_info(self):
        description = click.prompt('Please enter description for contract', type=str)
        totalAmount = click.prompt('Please enter contract money amount', type=int)
        return description, totalAmount

    def pick_client(self, clients):
        for c in clients:
            click.echo(f'{c.id} : {c.firstName} {c.firstName} ({c.company.name})')
        client_id = click.prompt('Please pick a client', type=int)
        return client_id
      
class EventView(View):
    def detail(self, event):
        click.echo(f'{event.id}: {event.name} ({event.contract.client.company.name}) debut:{event.startDate} fin:{event.endDate} ' +\
                   f'attendees:{event.attendees} location:{event.location.address}')

class LocationView(View):
    """"""

    def run(self):
        self.address = click.prompt('Please enter location address', type=str)
        return self.address