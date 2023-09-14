import click
# from src.controller import Controller
from src.controllers.dbcontroller import DbController
from src.controllers.usercontroller import UserController

__appname = "EPIC EVENTS"
__tablenames = ['user', 'client', 'contract', 'event']

# c = Controller()

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
def login():
    c = UserController()
    c.login()

# @cli.command()
# @click.option('-o',help="check")
# def login(o):
#     """
#     Prompt user for login credentials and authenticate to app.
#     -o check : Doesn't prompt. Just checks current token validity"""
#     if o == 'check':
#         c.verify_auth()
#     else:
#         c.auth_user()

@cli.command()
@click.argument('table')
@click.option('-o',help="mine")
def list(table, o):
    """
    list client/contract/event
    options : mine
    """
    check_table_name(table)    
    c.list(table,option=o)

@cli.command()
@click.argument('table')
def create(table):
    """
    create client/contract/event
    """    
    check_table_name(table)
    c.create(table)

@cli.command()
@click.argument('table')
def update(table):
    """
    update client/contract/event
    """    
    check_table_name(table)
    c.update(table)


def check_table_name(table):
    if table not in __tablenames:
        click.echo(f'{table} is not a valid object type. Please try user, client, contract or event')
        exit()

if __name__ == '__main__':
    cli()