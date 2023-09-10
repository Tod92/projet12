import click
from src.crud import delete_database, recreate_database, populate_database
from src.controller import Controller

__appname = "EPIC EVENTS"

c = Controller()

@click.group
def cli():
    click.echo(f'Welcome to {__appname}')
    pass

@cli.command()
def login():
    c.auth_user()

# @cli.command()
# def checklogin():
#     c.verify_auth()

@cli.command()
def populatedb():
    populate_database()
    click.echo('Populated the database')

@cli.command()
def initdb():
    recreate_database()
    click.echo('Initialized the database')

# @cli.command()
# def dropdb():
#     delete_database()
#     click.echo('Dropped the database')

@cli.command()
def listclients():
    c.list('client')
    
@cli.command()
def listcontracts():
    c.list('contract')
    
@cli.command()
def listevents():
    c.list('event')
    
@cli.command()
def createlocation():
    c.create('location')

@cli.command()
def createuser():
    c.create('user')

@cli.command()
def createcontract():
    c.create('contract')

@cli.command()
def createevent():
    c.create('event')

if __name__ == '__main__':
    cli()