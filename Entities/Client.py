from Entities.DBconfig import *


class Client(BaseModel):
    name = CharField()
    surname = CharField()
    pesel = IntegerField()
