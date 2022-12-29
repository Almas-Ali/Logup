from peewee import *
import string
import random
from datetime import datetime as dt

_logup = '.logup'
db = SqliteDatabase(_logup)


def ID_Gen():
    alpha = string.ascii_letters + string.digits
    ID = ''.join(random.sample(alpha, 8))
    return ID


class BaseLogup(Model):
    class Meta:
        database = db


class User(BaseLogup):
    id = AutoField()
    name = CharField(max_length=50)
    email = CharField(max_length=50, unique=True)
    username = CharField(max_length=50, unique=True)
    password = CharField(max_length=500)
    created_at = DateTimeField(default=dt.now())
    updated_at = DateTimeField(default=dt.now())

    def logs(self):
        return LogupDB.select().where(LogupDB.user == self)

    def __str__(self):
        return self.name


class LogupDB(BaseLogup):
    id = CharField(max_length=8, default=ID_Gen())
    content = TextField()
    user = ForeignKeyField(model=User, backref='logup_user')
    time = DateTimeField(default=dt.now())
