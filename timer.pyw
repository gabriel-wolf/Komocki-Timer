import tkinter as tk
from tkinter import Frame, RAISED, BOTH, BOTTOM, RIGHT, LEFT, SW, SE, StringVar
import datetime
from pygame import mixer


class Countdown(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # setup variables
        global alarm_choose,startText, stopText, language
        startText = StringVar()
        stopText = StringVar()
        language = StringVar()
        alarm_choose = "Analog"
        startText.set("Comienzo")
        stopText.set("Detener")
        language.set("Español")
        # run creat_widgets and show_widgets
        self.create_widgets()
        self.show_widgets()
        # set init vars for timer
        self.seconds_left = 0
        self._timer_on = False
        # setup music mixer
        mixer.init()
        mixer.music.load("" + alarm_choose + ".mp3")


    def show_widgets(self):
        # pack main level widgets
        self.label.pack(side = RIGHT, padx = 10)
        self.entry.pack(padx = 5, pady = 5)
        self.start.pack(padx = 1, pady = 1)
        self.stop.pack(padx = 1, pady = 1)
        # pack bottom level widgets
        self.sound.pack(side = LEFT, anchor = SW, padx = 1, pady = 1)
        self.languagepicker.pack(side = RIGHT, anchor = SE, padx = 1, pady = 1)


    def create_widgets(self):
        global alarm_choose, startText, stopText, language
        # create bottom level frame
        frame = Frame(self, relief=RAISED, borderwidth=1)
        frame.pack(fill=BOTH, side = BOTTOM, expand=True)
        # create main level contents
        self.label = tk.Label(self, text="00:00:00", fg = "blue", font = "Calibri 25 bold")
        self.entry = tk.Entry(self, justify='center')
        self.entry.focus_set()
        self.start = tk.Button(self, textvariable=startText, command=self.start_button, bg = "light green")
        self.stop = tk.Button(self, textvariable=stopText, command=self.stop_timer, bg = "#ff887f")
        # create bottom level contents
        self.languagepicker = tk.Button(frame, textvariable=language, command=self.switch_language)
        self.variable = tk.StringVar()
        self.variable.set("Analog") # default value
        options = ["Analog", "Tornado", "Purge"]
        self.sound = tk.OptionMenu(frame, self.variable, *options,  command=self.func)


    def switch_language(self):
        global language
        # determine which language to change
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
        # load in newly chosen sound into mixer
        alarm_choose = value
        mixer.music.load("" + value + ".mp3")


    def countdown(self):
        global alarm_choose
        # update label based on time left
        self.label['text'] = self.convert_seconds_left_to_time()
        # if times not up
        if self.seconds_left:
            self.seconds_left -= 1
            self._timer_on = self.after(1000, self.countdown)
        # else if time is up
        elif self.seconds_left <= 0:
            mixer.music.load("" + alarm_choose + ".mp3")
            mixer.music.play()
        # else
        else:
            self._timer_on = False


    def start_button(self):
        mixer.music.stop()
        self.seconds_left = int(self.entry.get())
        self.stop_timer()
        # switch to repeat in the correct language
        if language.get() == "Español":
            startText.set("Repetir")
        else:
            startText.set("Repeat")
        self.countdown()


    def stop_timer(self):
        # if timer is going
        if self._timer_on:
            self.start.config(bg = "light green")
            # set start button back to start in the correct language
            if language.get() == "Español":
                startText.set("Comienzo")
            else:
                startText.set("Start")
            self.after_cancel(self._timer_on)
            self._timer_on = False
            mixer.music.stop()


    def convert_seconds_left_to_time(self):
        # convert seconds left to time to display
        return datetime.timedelta(seconds=self.seconds_left)


if __name__ == '__main__':
    # set root options
    root = tk.Tk()
    root.title("Komocki Timer")
    root.resizable(False, False)
    countdown = Countdown(root)
    countdown.pack()
    root.mainloop()
