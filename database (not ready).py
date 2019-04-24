from peewee import *


db = PostgresqlDatabase(database="test_database", user="tester", password="test_password", host='localhost')
db.connect()


class DataBasePackage(Model):
    name = CharField()
    year = DateField()
    author = CharField()
    competition_name = CharField()
    complexity = SmallIntegerField()

    class Meta:
        database = db  # модель будет использовать базу данных 'people.db'


class DataBaseQuestion(Model):
    text = TextField()
    answer = TextField()
    complexity = SmallIntegerField()
    package = ForeignKeyField(DataBasePackage, backref="questions")

    class Meta:
        database = db


class DataBaseGame(Model):
    name = CharField()
    participants = []

    class Meta:
        database = db


db.create_tables([DataBaseQuestion, DataBasePackage, DataBaseGame])
