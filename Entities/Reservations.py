from Entities.DBconfig import *
from Entities.Client import Client
from Entities.Rooms import Rooms


class Reservation(BaseModel):
    client = ForeignKeyField(Client, backref='reservations')
    room = ForeignKeyField(Rooms, backref='reservations')
    is_active = BooleanField()
