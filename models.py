from peewee import *


identify = open("login.txt", "r")
login = identify.readlines()
identify.close()
db = PostgresqlDatabase(login[0], user=login[0])


def build_table():
    db.connect()
    db.drop_tables([UserStory], safe=True, cascade=True)
    db.create_tables([UserStory], safe=True)


class BaseModel(Model):

    class Meta:
        database = db


class UserStory(BaseModel):
    title = CharField()
    story = CharField()
    criteria = CharField()
    value = IntegerField()
    estimation = FloatField()
    status = CharField()

    class Meta:
        constraints = [Check("value BETWEEN 100 AND 1500"),
                       Check("estimation BETWEEN 0.5 AND 40"), Check("status = 'Planning' OR status = 'To Do' OR status = 'In Progress' OR status = 'Review' OR status = 'Done'")]
build_table()
