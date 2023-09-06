import click
from src.crud import delete_database, recreate_database
from src.controller import add_location

__appname = "EPIC EVENTS"


@click.group
def cli():
    pass

@cli.command()
def initdb():
    recreate_database()
    click.echo('Initialized the database')

@cli.command()
def dropdb():
    delete_database()
    click.echo('Dropped the database')

@cli.command()
def startapp():
    click.echo(f'Welcome to {__appname}')

@cli.command()
def addlocation():
    add_location()


if __name__ == '__main__':
    cli()