from peewee import *

db = PostgresqlDatabase('ChatbotDB', user='postgres', password='admin',
                        host='localhost', port=5432)
db.connect()


class BaseModel(Model):

    class Meta:
        database = db
