from tkinter import *
from chat import Hotel
from asr import detect_asr

BG_GREY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 14 bold"


def send_asr(msg, btn, a):
    detect_asr(msg, btn, a)


class ChatApp:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        self.hotel = Hotel(self)

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=670, height=550, bg=BG_COLOR)

        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR, text="Chat application", font=FONT_BOLD, pady=6)
        head_label.place(relwidth=1)

        divider = Label(self.window, width=400, bg=BG_GREY)
        divider.place(relwidth=1, rely=0.07, relheight=0.01)

        self.text_area = Text(self.window, width=25, height=2, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, padx=5, pady=5,
                              cursor="arrow", state=DISABLED, wrap=WORD)
        self.text_area.place(relheight=0.745, relwidth=1, rely=0.08)

        scrollbar = Scrollbar(self.text_area, command=self.text_area.yview)
        scrollbar.place(relheight=1, relx=0.974)

        self.bot_label = Label(self.window, bg=BG_GREY, height=80)
        self.bot_label.place(relwidth=1, rely=0.825)

        self.stringvar = StringVar()
        self.msg = Entry(self.bot_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT, )
        self.msg.place(relwidth=0.52, relheight=0.06, rely=0.008, relx=0.011)
        self.msg.focus()
        self.msg.bind("<Return>", self._on_send)

        self.send_btn = Button(self.bot_label, text="Send", font=FONT_BOLD, width=25, bg=BG_GREY,
                               command=lambda: self._on_send(None))
        self.send_btn.place(relx=0.55, rely=0.008, relheight=0.06, relwidth=0.22)

        self.asr_button = Button(self.bot_label, text="ASR", font=FONT_BOLD, width=25, bg=BG_GREY)
        self.asr_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        self.asr_button.configure(command=lambda: send_asr(self.msg, self.asr_button, self.send_btn))

    def _on_send(self, _):
        m = self.msg.get()
        self.insert_message(m, "You")

    def insert_message(self, m, sender):
        if not m:
            return
        self.msg.delete(0, END)

        m1 = f"{sender}: {m}\n\n"
        self.text_area.configure(state=NORMAL)
        self.text_area.insert(END, m1)
        self.text_area.configure(state=DISABLED)
        self.hotel.get_response(m)

    def insert_response(self, response):
        m2 = f"{self.hotel.bot_name}: {response}\n\n"
        self.text_area.configure(state=NORMAL)
        self.text_area.insert(END, m2)
        self.text_area.configure(state=DISABLED)

        self.text_area.see(END)

    def insert_input(self):
        msg_input = Entry(self.bot_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        msg_input.place(relwidth=0.52, relheight=0.06, rely=0.008, relx=0.011)
        msg_input.focus()
        input_btn = Button(self.bot_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GREY,
                           command=lambda: self.stringvar.set(msg_input.get()))
        input_btn.place(relx=0.55, rely=0.008, relheight=0.06, relwidth=0.22)

        msg_input.bind("<Return>", lambda event: input_btn.invoke())

        asr_input = Button(self.bot_label, text="ASR", font=FONT_BOLD, width=25, bg=BG_GREY)
        asr_input.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        asr_input.configure(command=lambda: send_asr(msg_input, asr_input, input_btn))

        input_btn.wait_variable(self.stringvar)
        m = self.stringvar.get()

        input_btn.destroy()
        msg_input.destroy()
        asr_input.destroy()

        m1 = f"You: {m}\n\n"
        self.text_area.configure(state=NORMAL)
        self.text_area.insert(END, m1)
        self.text_area.configure(state=DISABLED)

        self.msg.focus()
        return m


if __name__ == "__main__":
    app = ChatApp()
    app.run()
