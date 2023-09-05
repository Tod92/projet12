import click
from crud import delete_database, recreate_database


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

if __name__ == '__main__':
    cli()