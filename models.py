from peewee import *


class CreateDatabase:
    @staticmethod
    def create_db_object():
        identify = open("db.txt", "r")
        login = identify.readlines()
        identify.close()
        db = PostgresqlDatabase(login[0], user=login[0])
        return db


class BaseModel(Model):
    class Meta:
        database = CreateDatabase.create_db_object()


class Entries(BaseModel):
    story_title = CharField()
    user_story = CharField()
    acceptance_criteria = CharField()
    business_value = IntegerField()
    estimation = FloatField()
    status = CharField()
