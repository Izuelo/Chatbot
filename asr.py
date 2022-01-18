import sys
import threading
from tkinter import Entry, Button, NORMAL, DISABLED

import speech_recognition as sr


def detect_asr(msg, btn, send_btn):
    r = sr.Recognizer()
    mic = sr.Microphone()
    t = threading.Thread(target=asr, args=(r, mic, msg, btn, send_btn))
    t.start()


def asr(r, mic, msg: Entry, btn: Button, send_btn: Button):
    btn.configure(state=DISABLED, bg="#800000")
    text = ""
    while text != "send":
        with mic as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)

            try:
                text = r.recognize_google(audio, language="en-EN")
            except sr.RequestError:
                text = ""
            except sr.UnknownValueError:
                text = ""
            finally:
                if text != "send":
                    msg.insert(len(msg.get()), text)
    btn.configure(state=NORMAL, bg="#ABB2B9")
    send_btn.invoke()
    sys.exit()
