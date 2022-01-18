import random
import json
import torch

from interactions import check_for_room, make_reservation, list_of_reservations
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize, nltk_tagger
from tts import play_tts


class Hotel:
    def __init__(self, chatbot):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.chatbot = chatbot
        with open("intents.json", "r") as f:
            self.intents = json.load(f)

        self.FILE = "data.pth"
        self.data = torch.load(self.FILE)
        self.input_size = self.data["input_size"]
        self.hidden_size = self.data["hidden_size"]
        self.output_size = self.data["output_size"]
        self.all_words = self.data["all_words"]
        self.tags = self.data["tags"]
        self.model_state = self.data["model_state"]

        self.model = NeuralNet(self.input_size, self.hidden_size, self.output_size).to(self.device)
        self.model.load_state_dict(self.model_state)
        self.model.eval()
        self.bot_name = "Sam"

    def get_response(self, sentence):
        sentence = tokenize(sentence)
        sentence_nums = nltk_tagger(sentence)
        x = bag_of_words(sentence, self.all_words)
        x = x.reshape(1, x.shape[0])
        x = torch.from_numpy(x)

        output = self.model(x)
        _, predicted = torch.max(output, dim=1)
        tag = self.tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        interactions_tags = ["rooms", "reserve", "my reservations"]
        if prob.item() > 0.75:
            for intent in self.intents["intents"]:
                if tag == intent["tag"] and intent["tag"] == "rooms":
                    check_for_room(self.bot_name, sentence_nums, intent, self.chatbot)
                if tag == intent["tag"] and intent["tag"] == "reserve":
                    make_reservation(self.bot_name, intent, self.chatbot)
                if tag == intent["tag"] and intent["tag"] == "my reservations":
                    list_of_reservations(self.bot_name, intent, self.chatbot)
                elif tag == intent["tag"] and tag not in interactions_tags:
                    say = random.choice(intent['responses'])
                    self.chatbot.insert_response(say)
                    play_tts(say)
        else:
            say = "I don't understand... Could you rephrase the question?"
            self.chatbot.insert_response(say)
            play_tts(say)

