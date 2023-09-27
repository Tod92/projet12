import click
from src.controllers.dbcontroller import DbController
from src.controllers.authcontroller import AuthController
from src.controllers.usercontroller import UserController
from src.controllers.clientcontroller import ClientController
from src.controllers.contractcontroller import ContractController
from src.controllers.eventcontroller import EventController

__appname = "EPIC EVENTS"
__tablenames = ['user', 'client', 'contract', 'event']


@click.group
def cli():
    click.echo(f'Welcome to {__appname}')
    pass

@cli.command()
def initdb():
    c = DbController()
    c.init_tables()
    click.echo('Initialized the database')

@cli.command()
def populatedb():
    c = DbController()
    c.populate_database()
    # click.echo('Populated the database')


@cli.command()
@click.option('-o',help="check")
def login(o):
    """
    Prompt user for login credentials and authenticate to app.
    -o checkonly : Doesn't prompt. Just checks current token validity
    """
    c = AuthController()
    if o == 'check':
        c.verify_auth()
    else:
        c.login()

@cli.command()
@click.argument('table')
@click.option('-o',help="mine / nosupport")
def list(table, o):
    """
    list client/contract/event
    options : mine nosupport(event) tosign(contract) topay(contract)
    """
    c = get_table_controller(table)  
    c.list(option=o)

@cli.command()
@click.argument('table')
def create(table):
    """
    create client/contract/event
    """    
    c = get_table_controller(table)
    c.create(table)

@cli.command()
@click.argument('table')
def update(table):
    """
    update client/contract/event
    """    
    c = get_table_controller(table)
    c.update(table)


def get_table_controller(table):
    if table not in __tablenames:
        click.echo(f'{table} is not a valid object type. Please try user, client, contract or event')
        exit()
    elif table == 'user':
        return UserController()
    elif table == 'client':
        return ClientController()
    elif table == 'contract':
        return ContractController()
    elif table == 'event':
        return EventController()
    
if __name__ == '__main__':
    cli()