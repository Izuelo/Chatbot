from gtts import gTTS
from playsound import playsound
import os


def play_tts(sentence):
    tts = gTTS(text=sentence, lang="en", tld="com", slow=False)
    tts.save("tts.mp3")
    play_sound()


def play_sound():
    path = (os.path.dirname(__file__) + "\\tts.mp3")
    playsound(path)

