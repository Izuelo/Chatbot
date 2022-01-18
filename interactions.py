import random
from Entities.Client import Client
from Entities.Reservations import Reservation
from Entities.Rooms import Rooms
from tts import play_tts


def check_for_room(bot_name, sentence_nums, intent, chatbot):
    say = random.choice(intent['responses'])
    chatbot.insert_response(say)
    play_tts(say)
    if sentence_nums:
        number_of_rooms = Rooms.select().where(
            Rooms.is_available == True and Rooms.room_size == sentence_nums[0]).count()
    else:
        number_of_rooms = Rooms.select().where(
            Rooms.is_available == True).count()
    say = f"There are {number_of_rooms} room(s) available at this moment"
    chatbot.insert_response(say)
    play_tts(say)
    if number_of_rooms == 0:
        say = "We are sorry that there is no room at our hotel"
        chatbot.insert_response(say)
        play_tts(say)


def make_reservation(bot_name, intent,chatbot):
    say = random.choice(intent['responses'])
    chatbot.insert_response(say)
    play_tts(say)

    room = Rooms.select().where(Rooms.is_available == True)
    if room.exists():
        name = input()
        surname = input("Last name >> ")
        pesel = input("PESEL >> ")

        client = Client.select().where(Client.pesel == pesel)
        if client.exists():
            client = Client.select().where(Client.pesel == pesel).get()
        else:
            client = Client(name=name, surname=surname, pesel=pesel)
            client.save()

        room = room.get()
        room.is_available = False
        room.save()
        reservation = Reservation(client=client, room=room, is_active=True)
        reservation.save()
        say = f"Your reservation was successful {name}. Your room number is {room.room_number}"
        chatbot.insert_response(say)
        play_tts(say)
    else:
        say = "There are no rooms available. We are sorry :C"
        chatbot.insert_response(say)
        play_tts(say)


def list_of_reservations(bot_name, intent,chatbot):
    say = random.choice(intent['responses'])
    chatbot.insert_response(say)
    play_tts(say)

    pesel = input("PESEL >> ")

    say = "I'm collecting all your reservations and will list them in a moment"
    chatbot.insert_response(say)
    play_tts(say)

    client = Client.select().where(Client.pesel == pesel)
    rooms_nr = []
    if client.exists():
        client = Client.select().where(Client.pesel == pesel).get()
        for row in client.reservations:
            if row.is_active:
                rooms_nr.append(str(row.room.room_number))

        if len(rooms_nr) > 0:
            rooms_nr = ', '.join(rooms_nr)
            say = f"{client.name}, your reserved rooms are: {rooms_nr} ."
            chatbot.insert_response(say)
            play_tts(say)
        else:
            say = f"{client.name}, you dont have any reservations active."
            chatbot.insert_response(say)
            play_tts(say)
    else:
        say = "Incorrect PESEL number."
        chatbot.insert_response(say)
        play_tts(say)
