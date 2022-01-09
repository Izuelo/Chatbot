from Entities.Reservations import Reservation
from Entities.Client import Client
from Entities.Rooms import Rooms
from Entities.DBconfig import db

db.create_tables([Client, Rooms, Reservation])
