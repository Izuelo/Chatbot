from Entities.DBconfig import *


class Rooms(BaseModel):
    room_number = IntegerField()
    is_available = BooleanField()
    room_size = IntegerField()
