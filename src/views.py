import click
import datetime





class View:

    def permission_denied(self):
        click.echo("PERMISSION DENIED !!")

    def get_date(self, msg):
        click.echo(msg)
        day = click.prompt('please enter DAY :', type=int)
        month = click.prompt('please enter MONTH :', type=int)
        year = click.prompt('please enter YEAR :', type=int)
        date = datetime.date(year=year, month=month, day=day)
        return date
    
    def get_str(self, msg, max_length=200):
        result = ''
        first = True
        while result == '' or len(result) > max_length:
            if first == False:
                click.echo(f'Please respect max length ({max_length})')
            result = click.prompt(f'please enter {msg} :', type=str)
            first = False
        return result

    def get_int(self, msg, max=None):
        while True:
            result = click.prompt(f'please enter {msg} :', type=int)
            if max:
                if result > max:
                    click.echo('please respect maximum value ({max})')
                    continue
            return result

    def get_password(self):
        self.password = click.prompt('Please enter password', type=str)
        return self.password 
    def creation_starting(self, table):
         click.echo(f'---Starting {table} creation process ---')

    def creation_completed(self, table):
         click.echo(f'--- Creation of {table} completed ---')
    
    def update_completed(self):
        click.echo('--- Update completed ! ---')

    def not_found(self, object_type=''):
        click.echo(f'{object_type} not found !')

    def exiting(self):
        click.echo('--- Exiting app ---')

    def unknown_object(self, description='this'):
        click.echo()

    def pick_in_list(self, instances, prompt=True):
        """
        Asks to choose instance object list.
        Exits if instances list empty.
        Returns id.
        prompt=False to simply show list  
        """
        if len(instances) == 0:
            self.not_found()
            self.exiting()
            exit()
        
        for i in instances:
            self.list_item(i)
        tablename = instances[0].__tablename__
        if prompt == False:
            return None
        else:
            return click.prompt(f'Please pick a {tablename}', type=int)    

    def pick_in_attr(self, attr_list, instance):
        """
        Asks user to pick an attribute of instance within attr_list.
        Returns index in attr_list for delected attribute
        """
        click.echo(f'Attribute selection for {instance} --')
        count = 0
        instance_attr = instance.__dict__
        for attr in attr_list:
            count += 1
            click.echo(f'{count}: {attr} : {instance_attr[attr]} ')
        return click.prompt(f'Please pick attribute', type=int) - 1
    
    def list_item(self, item):
        click.echo(f'{item.id} : {item}')


class AuthView(View):
    """"""

    def get_login(self):
        self.login = click.prompt('Please enter login', type=str)
        return self.login
        
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
        

class ClientView(View):
    def detail(self, client):
        click.echo(f'{client.id}:{client.firstName} {client.lastName} {client.email} phone:{client.phone} company:{client.company.name} ' +\
                   f'created:{client.creationDate} last update:{client.lastUpdateDate} commercial:{client.commercialContact}')
 
    def get_info(self):
        firstName = self.get_str('Please enter first name', max_length=50)
        lastName = self.get_str('Please enter last name', max_length=50)
        email = self.get_str('Please enter email', max_length=50)
        phone = self.get_int('Please enter phone', max=9999999999)
        return firstName, lastName, email, phone

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

      
class EventView(View):
    def detail(self, event):
        click.echo(f'{event.id}: {event.name} ({event.contract.client.company.name}) debut:{event.startDate} fin:{event.endDate} ' +\
                   f'attendees:{event.attendees} location:{event.location.address}')

    def get_info(self):
        startDate = self.get_date('Please enter start date')
        endDate = self.get_date('Please enter end date')
        attendees = click.prompt('Please enter number of attendees', type=int)
        notes = click.prompt('Please enter notes', type=str)
        return startDate, endDate, attendees, notes

    def no_contract_found(self):
        click.echo('No contract found to create an event from !')


class LocationView(View):
    """"""

    def run(self):
        self.address = click.prompt('Please enter location address', type=str)
        return self.address