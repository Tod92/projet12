import click
from src.crud import delete_database, recreate_database, populate_database
from src.controller import add_location, auth_user

__appname = "EPIC EVENTS"


@click.group
def cli():
    click.echo(f'Welcome to {__appname}')
    pass

@cli.command()
def login():
    auth_user()

@cli.command()
def populatedb():
    populate_database()
    click.echo('Populated the database')

@cli.command()
def initdb():
    recreate_database()
    click.echo('Initialized the database')

@cli.command()
def dropdb():
    delete_database()
    click.echo('Dropped the database')

 

@cli.command()
def addlocation():
    add_location()


if __name__ == '__main__':
    cli()