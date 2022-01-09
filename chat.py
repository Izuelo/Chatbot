import random
import json
import torch

from Entities.Client import Client
from Entities.Reservations import Reservation
from Entities.Rooms import Rooms
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize, nltk_tagger

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

with open("intents.json", "r") as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

enable_chat = True
bot_name = "Sam"
print("Let's chat! type 'quit' to exit")


def check_for_room():
    print(f"{bot_name}: {random.choice(intent['responses'])}")
    if sentence_nums:
        number_of_rooms = Rooms.select().where(
            Rooms.is_available == True and Rooms.room_size == sentence_nums[0]).count()
    else:
        number_of_rooms = Rooms.select().where(
            Rooms.is_available == True).count()
    print(f"{bot_name}: There are {number_of_rooms} room(s) available at this moment")


def make_reservation():
    print(f"{bot_name}: {random.choice(intent['responses'])}")

    room = Rooms.select().where(Rooms.is_available == True)
    if room.exists():
        name = input("First name >> ")
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
    else:
        print(f"{bot_name}: There are no rooms available. We are sorry :C")


while enable_chat:
    sentence = input("You: ")
    if sentence == "quit":
        enable_chat = False
    else:
        sentence = tokenize(sentence)
        sentence_nums = nltk_tagger(sentence)
        x = bag_of_words(sentence, all_words)
        x = x.reshape(1, x.shape[0])
        x = torch.from_numpy(x)

        output = model(x)
        _, predicted = torch.max(output, dim=1)
        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]

        if prob.item() > 0.75:
            for intent in intents["intents"]:
                if tag == intent["tag"] and intent["tag"] == "rooms":
                    check_for_room()
                if tag == intent["tag"] and intent["tag"] == "reserve":
                    make_reservation()
                elif tag == intent["tag"]:
                    print(f"{bot_name}: {random.choice(intent['responses'])}")
        else:
            print(f"{bot_name}: I don't understand... Could you rephrase the question?")
