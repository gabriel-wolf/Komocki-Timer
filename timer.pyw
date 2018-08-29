import tkinter as tk
from tkinter import Frame, RAISED, BOTH, BOTTOM, RIGHT, LEFT, SW, SE, StringVar
import datetime
from pygame import mixer


class Countdown(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        global alarm_choose,startText, stopText, language
        startText = StringVar()
        stopText = StringVar()
        language = StringVar()
        alarm_choose = "Analog"
        startText.set("Comienzo")
        stopText.set("Detener")
        language.set("Español")
        self.create_widgets()
        self.show_widgets()
        self.seconds_left = 0
        self._timer_on = False
        mixer.init()
        mixer.music.load("" + alarm_choose + ".mp3")


    def show_widgets(self):
        self.label.pack(side = RIGHT, padx = 10)
        self.entry.pack(padx = 5, pady = 5)
        self.start.pack(padx = 1, pady = 1)
        self.stop.pack(padx = 1, pady = 1)
        self.sound.pack(side = LEFT, anchor = SW, padx = 1, pady = 1)
        self.languagepicker.pack(side = RIGHT, anchor = SE, padx = 1, pady = 1)


    def create_widgets(self):
        global alarm_choose, startText, stopText, language
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, side = BOTTOM, expand=True)
        self.label = tk.Label(self, text="00:00:00", fg = "blue", font = "Calibri 25 bold")
        self.entry = tk.Entry(self, justify='center')
        self.entry.focus_set()
        self.start = tk.Button(self, textvariable=startText, command=self.start_button, bg = "light green")
        self.stop = tk.Button(self, textvariable=stopText, command=self.stop_timer, bg = "#ff887f")
        self.languagepicker = tk.Button(frame, textvariable=language, command=self.switch_language)
        self.variable = tk.StringVar()
        self.variable.set("Analog")
        options = ["Analog", "Tornado", "Purge"]
        self.sound = tk.OptionMenu(frame, self.variable, *options,  command=self.func)


    def switch_language(self):
        global language
        if language.get() == "Español":
            language.set("English")
            startText.set("Start")
            self.start.config(bg = "light green")
            stopText.set("Stop")
        else:
            language.set("Español")
            self.start.config(bg = "light green")
            startText.set("Comienzo")
            stopText.set("Detener")


    def func(self,value):
        global alarm_choose
        alarm_choose = value
        mixer.music.load("" + value + ".mp3")


    def countdown(self):
        global alarm_choose
        self.label['text'] = self.convert_seconds_left_to_time()
        if self.seconds_left:
            self.seconds_left -= 1
            self._timer_on = self.after(1000, self.countdown)
        elif self.seconds_left <= 0:
            mixer.music.load("" + alarm_choose + ".mp3")
            mixer.music.play()
        else:
            self._timer_on = False


    def start_button(self):
        mixer.music.stop()
        self.seconds_left = int(self.entry.get())
        self.stop_timer()
        if language.get() == "Español":
            startText.set("Repetir")
        else:
            startText.set("Repeat")
        self.countdown()


    def stop_timer(self):
        if self._timer_on:
            self.start.config(bg = "light green")
            if language.get() == "Español":
                startText.set("Comienzo")
            else:
                startText.set("Start")
            self.after_cancel(self._timer_on)
            self._timer_on = False
            mixer.music.stop()


    def convert_seconds_left_to_time(self):
        return datetime.timedelta(seconds=self.seconds_left)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Komocki Timer")
    root.resizable(False, False)
    countdown = Countdown(root)
    countdown.pack()
    root.mainloop()
