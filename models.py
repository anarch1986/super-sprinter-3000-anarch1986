from peewee import *


class CreateDatabase:

    def create_db_object():
        identify = open("database_data.txt", "r")
        login = identify.readlines()
        identify.close()
        db = PostgresqlDatabase(login[0], user=login[0])
        return db


class BaseModel(Model):

    class Meta:
        database = CreateDatabase.create_db_object()


class UserStory(BaseModel):
    title = CharField(max_length=100)
    story = CharField(max_length=580)
    criteria = CharField(max_length=580)
    value = IntegerField()
    estimation = FloatField()
    status = CharField()

    class Meta:
        constraints = [Check("value BETWEEN 100 AND 1500"),
                       Check("estimation BETWEEN 0.5 AND 40"), Check("status = 'Planning' OR status = 'To Do' OR status = 'In Progress' OR status = 'Review' OR status = 'Done'")]