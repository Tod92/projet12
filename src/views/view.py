import click
import datetime

class View:
    """
    """
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
         click.echo(f'--- Creation of {table} item completed ---')
    
    def update_completed(self):
        click.echo('--- Update completed ! ---')

    def not_found(self, object_type=''):
        click.echo(f'{object_type} not found !')

    def exiting(self):
        click.echo('--- Exiting app ---')

    def list_instances(self, instances, prompt=False):
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
        tablename = instances[0].__tablename__
        for i in instances:
            self.list_item(i)
        if prompt == True:
            return click.prompt(f'Please pick a {tablename}', type=int)
        else:
            return None

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
    
