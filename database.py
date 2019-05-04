from peewee import *
from collections import OrderedDict

_database = PostgresqlDatabase(None)

def init_database(dict_args):
    _database.init(database=dict_args["database"], user=dict_args["user"],
                                         password=dict_args["password"],
                                         host=dict_args['host'])
    _database.drop_tables([DataBaseGame])
    _database.create_tables([DataBaseQuestion, DataBasePackage, DataBaseGame])
    return _database


class BaseModel(Model):
    class Meta:
        database = _database


class DataBasePackage(BaseModel):
    name = CharField(unique=True)
    author = CharField(null=True)
    complexity = SmallIntegerField(null=True)


class DataBaseQuestion(BaseModel):
    text = TextField(unique=True)
    comment = TextField(null=True)
    answer = TextField()
    name = TextField(null=True)
    author = CharField(null=True)
    complexity = SmallIntegerField(null=True, default=None)
    package = ForeignKeyField(DataBasePackage, backref="questions", null=True)


class DataBaseGame(BaseModel):
    name = CharField(null=True, unique=True)
    date = DateField(null=True)
    time = TimeField(null=True)
    table = TextField(default="{}")
    previous = BooleanField(default=True)
