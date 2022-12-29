import os
import hashlib
import typer
import glob
from models import User, LogupDB, db
from rong import Text
from tabulate import tabulate


_logup = '.logup'
_logup_cache = '.logup_cache'
__version__ = '0.0.1'
__author__ = 'Md. Almas Ali'

app = typer.Typer(
    add_completion=False,
    help='Logup is a simple CLI utility to keep track of your logs encryptedly.',
    name='logup',
    epilog=Text(text=f'Developed by {__author__} | Version: {__version__}', fg='cyan', styles=[
                'bold', 'underline-dashed']).__str__(),
)


def is_db_exists():
    '''Check if database exists'''
    LOG_DB = glob.glob(_logup)
    if LOG_DB == []:
        return False
    else:
        return True


def hash_password(password: str):
    '''Hash password'''

    hash_object = hashlib.sha512()
    hash_object.update(password.encode('utf-8'))

    return hash_object.hexdigest().strip()


def match_password(password: str, hashed_password: str):
    '''Match password'''
    if hash_password(password=password) == hashed_password:
        return True
    else:
        return False


def user_validation(username: str, password: str):
    '''Validate user credentials'''
    try:
        _user = User.get(User.username == username)
        if _user.password == password:
            return True
        else:
            return False

    except Exception as e:
        print(e)
        return False


def add_cache(username: str, password: str):
    '''Add cache user credentials'''
    if is_cache_exists():
        Text('[!] Cache already exists! ', fg='red', styles=['bold']).print()
        return

    if user_validation(username=username, password=password):
        with open(_logup_cache, 'w') as f:
            f.write(username+'\n')
            f.write(password)
    else:
        return False


def remove_cache():
    '''Remove cached user credentials'''
    if os.path.exists(_logup_cache):
        os.remove(_logup_cache)
    else:
        return False


def get_cache():
    '''Get cached user credentials'''
    if os.path.exists(_logup_cache):
        with open(_logup_cache, 'r') as f:
            username = f.readline().strip()
            password = f.readline().strip()
            return username, password
    else:
        return False


def is_cache_exists():
    '''Check if cache exists'''
    if os.path.exists(_logup_cache):
        return True
    else:
        return False




@app.command(
    help='Initialize Logup database. This command will create a database file in the current directory.',
    name='init'
)
def init():
    '''Initialize Logup database. This command will create a database file in the current directory.'''

    if not is_db_exists():
        try:
            db.create_tables([User, LogupDB])
            Text(text='[+] Successfully created Logup database. ',
                 fg='green', styles=['bold']).print()

        except Exception as e:
            print(e)
            Text(text='[!] Failed to create Logup database ! ',
                 fg='red', styles=['bold']).print()
    else:
        Text('[!] Logs already exist! ', fg='red', styles=['bold']).print()


@app.command(
    help='Cache user credentials.', name='addcache'
)
def addcache(username: str = None, password: str = None):
    '''Cache user credentials.'''

    if not is_db_exists():
        Text('[!] Logup isn\'t initialized yet! ',
             fg='red', styles=['bold']).print()
        return

    if username == None:
        username = typer.prompt('Enter username')
    if password == None:
        password = typer.prompt(
            'Enter password (minimum 8 charecters)', hide_input=True)
    password = hash_password(password=password)
    

    if user_validation(username=username, password=password):
        add_cache(username=username, password=password)
        Text('[+] Successfully cached user credentials. ',
             fg='green', styles=['bold']).print()
    else:
        Text('[!] Invalid credentials! ', fg='red', styles=['bold']).print()


@app.command(
    help='Remove cached user credentials.', name='removecache'
)
def removecache():
    '''Remove cached user credentials.'''

    if not is_db_exists():
        Text('[!] Logup isn\'t initialized yet! ',
             fg='red', styles=['bold']).print()
        return

    if is_cache_exists():
        remove_cache()
        Text('[+] Successfully removed cached user credentials. ',
             fg='green', styles=['bold']).print()
    else:
        Text('[!] No cached credentials found! ',
             fg='red', styles=['bold']).print()


@app.command(
    help='Is cached user credentials exists?', name='iscache'
)
def iscache():
    '''Is cached user credentials exists?'''

    if not is_db_exists():
        Text('[!] Logup isn\'t initialized yet! ',
             fg='red', styles=['bold']).print()
        return

    if is_cache_exists():
        Text('[+] Cached user credentials exists. ',
             fg='green', styles=['bold']).print()
    else:
        Text('[!] No cached credentials found! ',
             fg='red', styles=['bold']).print()


@app.command(
    help='Show logs from the database.', name='logs'
)
def logs(username: str = None, password: str = None):
    '''Show logs from the database.'''

    if not is_db_exists():
        Text('[!] Logup isn\'t initialized yet! ',
             fg='red', styles=['bold']).print()
        return

    if is_cache_exists():
        username, password = get_cache()

    if username == None:
        username = typer.prompt('Enter username')
    if password == None:
        password = typer.prompt('Enter password', hide_input=True)
        password = hash_password(password=password)

    if user_validation(username=username, password=password):
        try:
            _user = User.get(User.username == username)
            _log = LogupDB.select().where(LogupDB.user == _user).dicts()
            for i in _log:
                __user = User.get(User.id == i['user'])
                i['user'] = __user.name
            print(tabulate(_log, headers='keys', tablefmt='psql'))

        except Exception as e:
            print(e)
            Text('[!] No logs found! ', fg='red', styles=['bold']).print()
    else:
        Text('[!] Invalid credentials! ', fg='red', styles=['bold']).print()


@app.command(
    help='Add a log to the database.', name='add'
)
def add(username: str = None, password: str = None, content: str = None):
    '''Add a log to the database.'''

    if not is_db_exists():
        Text('[!] Logup isn\'t initialized yet! ',
             fg='red', styles=['bold']).print()
        return

    if is_cache_exists():
        username, password = get_cache()

    if username == None:
        username = typer.prompt('Enter username')
    if password == None:
        password = typer.prompt('Enter password', hide_input=True)
        password = hash_password(password=password)
    if content == None:
        content = typer.prompt('Enter log content')

    if user_validation(username=username, password=password):
        try:
            _user = User.get(User.username == username)
            LogupDB.create(user=_user, content=content)
            
            Text(text='[+] Log added.', fg='green', styles=['bold']).print()
        except Exception as e:
            print(e)
            Text('[!] Failed to add log ! ', fg='red', styles=['bold']).print()
    else:
        Text('[!] Invalid credentials! ', fg='red', styles=['bold']).print()


@app.command(
    help='Add a user to the database.', name='adduser'
)
def adduser(name: str = None,
            email: str = None,
            username: str = None,
            password: str = None
            ):
    '''Add a user to the database.'''

    if not is_db_exists():
        Text('[!] Logup isn\'t initialized yet! ',
             fg='red', styles=['bold']).print()
        return

    if is_cache_exists():
        username, password = get_cache()

    if name == None:
        name = typer.prompt('Enter user full name')
    if email == None:
        email = typer.prompt('Enter user email')
    if username == None:
        username = typer.prompt('Enter user username')
    if password == None:
        password = typer.prompt(
            'Enter user password (minimum 8 charecters)', hide_input=True, confirmation_prompt=True, min=8, max=32)

    try:
        _user = User.select().where(User.email == email)
        if _user.exists():
            Text('[!] User already exists! ',
                 fg='red', styles=['bold']).print()
            return

        _user = User.select().where(User.username == username)
        if _user.exists():
            Text('[!] Username already exists! ',
                 fg='red', styles=['bold']).print()
            return

        _password = hash_password(password=password)

        _user = User(name=name, email=email,
                     username=username, password=_password)
        _user.save()

        Text(text='[+] User added successfully!',
             fg='green', styles=['bold']).print()

    except Exception as e:
        print(e)
        Text('[!] Failed to add user ! ', fg='red', styles=['bold']).print()


@app.command(
    help='List all users from the database.', name='listuser'
)
def listuser(username: str = None, password: str = None):
    '''List all users from the database.'''

    if not is_db_exists():
        Text('[!] Logup isn\'t initialized yet! ',
             fg='red', styles=['bold']).print()
        return

    if is_cache_exists():
        username, password = get_cache()

    if username == None:
        username = typer.prompt('Enter username')
    if password == None:
        password = typer.prompt('Enter password', hide_input=True)
        password = hash_password(password=password)

    if user_validation(username=username, password=password):
        try:
            _users = User.select().dicts()
            for i in _users:
                del i['password']
                del i['created_at']
                del i['updated_at']
            print(tabulate(_users, headers='keys', tablefmt='psql'))

        except Exception as e:
            print(e)
            Text('[!] Failed to list users ! ',
                 fg='red', styles=['bold']).print()
    else:
        Text('[!] Invalid credentials! ', fg='red', styles=['bold']).print()


@app.command(
    help='Clear entire database.', name='clear'
)
def clear(username: str = None, password: str = None):
    '''Clear entire database.'''
    if not is_db_exists():
        Text('[!] Logup isn\'t initialized yet! ',
             fg='red', styles=['bold']).print()
        return

    if is_cache_exists():
        username, password = get_cache()

    if username == None:
        username = typer.prompt('Enter username')
    if password == None:
        password = typer.prompt('Enter password', hide_input=True)
        password = hash_password(password=password)

    if user_validation(username=username, password=password):
        try:
            os.remove(_logup)
            Text(text='[+] Successfully removed database.',
                 fg='green', styles=['bold']).print()
        except Exception as e:
            print(e)
            Text('[!] Failed to remove database!',
                 fg='red', styles=['bold']).print()
    else:
        Text('[!] Invalid credentials! ', fg='red', styles=['bold']).print()
