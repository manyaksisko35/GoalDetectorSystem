import serial
import threading
import time
from kivy.app import App
from kivy.uix.label import Label
from kivy.clock import Clock
import pygame

#Type your arduino uno port instead of COM3
ser = serial.Serial('COM3', 9600, timeout=1)  


pygame.mixer.init()
goal_sound = pygame.mixer.Sound("goal.mp3")  


class GoalApp(App):
    def build(self):
        self.label = Label(text="Gol bekleniyor...", font_size=72) #This is 'Waiting For Goal...'  text but turkish :)
        Clock.schedule_interval(self.update_label, 0.1)
        self.goal = False
        return self.label

    def update_label(self, dt):
        if self.goal:
            if int(time.time() * 2) % 2 == 0:
                self.label.text = "GOAL!!!"
            else:
                self.label.text = ""
        else:
            self.label.text = "Gol bekleniyor..." #This is 'Waiting For Goal...'  text but turkish :)


def read_serial(app):
    while True:
        line = ser.readline().decode().strip()
        if line == "GOAL":
            app.goal = True
            goal_sound.play()
            time.sleep(1) 
            app.goal = False


if __name__ == "__main__":
    app = GoalApp()
    t = threading.Thread(target=read_serial, args=(app,), daemon=True)
    t.start()
    app.run()
