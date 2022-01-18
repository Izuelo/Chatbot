import threading
from gtts import gTTS
from playsound import playsound
import os
import sys


def play_tts(sentence):
    t = threading.Thread(target=play_sound, kwargs={"s": sentence})
    t.start()


def play_sound(s):
    try:
        tts = gTTS(text=s, lang="en", tld="com", slow=False)
        tts.save("tts.mp3")
        path = (os.path.dirname(__file__) + "\\tts.mp3")
        playsound(path)
        os.remove(path)
    except PermissionError:
        pass
    finally:
        sys.exit()
