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
@click.option('-o',help="check")
def login(o):
    if o == 'check':
        c.verify_auth()
    else:
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

@cli.command()
@click.argument('table')
def list(table):
    c.list(table)

@cli.command()
@click.argument('table')
def create(table):
    c.create(table)


if __name__ == '__main__':
    cli()