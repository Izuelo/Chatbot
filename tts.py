import threading
from gtts import gTTS
from playsound import playsound
import os
import sys

thread_queue = []


def play_tts(sentence):
    t = threading.Thread(target=play_sound, kwargs={"s": sentence})
    thread_queue.append(t)
    if len(thread_queue) == 1:
        thread_queue[0].start()


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
        thread_queue.pop(0)
        if len(thread_queue) > 0:
            thread_queue[0].start()
        sys.exit()
