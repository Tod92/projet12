import click






class View:
    pass

class LocationView(View):
    """"""

    def run(self):
        self.address = click.prompt('Please enter location address', type=str)
        return self.address