# Epic Events

1. Why


    This is a proof of concept (POC) project to show a light-weight version of our CRM plateform, based on PostgresSql database. The aim is to keep track of data about clients, contracts and events. This app is working around user permissions depending on the user's role in the company (Gestion, Commercial or Support) :

    * Gestion : Can create/update app users and clients. Can create contracts associated to clients.

    * Commercial : Can create/update his clients. Can create events associated with signed contracts.

    * Support : Can update his events.


2. Getting Started

    This project uses the following technologies:

    * Python v3.x+

    * [SqlAlchemy](https://www.sqlalchemy.org/)

        Whereas Django does a lot of things for us out of the box, SqlAlchemy (+ sqlalchemy-orm) allows us to add only what we need. 
     

    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 
 
    * [Argon2](https://pypi.org/project/argon2-cffi/)

        This package manages password hashing for app users

    * [PyJWT](https://pyjwt.readthedocs.io/en/stable/)

        This token package is used for user's authentication. 

    * [Click](https://click.palletsprojects.com/en/8.1.x/)

        Used for light Command Line Interface
    
    * [Sentry-sdk](https://docs.sentry.io/platforms/python/)

       Will catch and log python exceptions in app


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Next, type <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Rather than hunting around for the packages you need, you can install in one step. Type <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file. If you install a package, make sure others know by updating the requirements.txt file. An easy way to do this is <code>pip freeze > requirements.txt</code>

    - A config.py file is needed for the application to launch. This file will contain sensible informations like sql database password and is not present in the actual git deposit. Please contact dev for more informations about this file

    - You should now be ready to test the application. In the "EpicEvent" directory, type <code>python app.py</code>. The app should respond with possible commands ie <code>python app.py login</code>

4. Current Setup

    The app is using [JSON file](https://www.tutorialspoint.com/json/json_quick_guide.htm) to populate the database. To use those tests objects in the app please follow :

    <code>python app.py initdb</code>
    <code>python app.py populatedb</code>

    You should then be able to login with any user credentials present in the population.json file.
     
      
