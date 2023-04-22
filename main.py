
import kivy
import numpy as np
import time
from kivy.clock import Clock
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line, Ellipse
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.factory import Factory
from kivymd.app import MDApp
from kivy import factory
from functools import partial

# importing a file greatgatsby.txt into array of strings
def generate_words():
    file = np.genfromtxt('greatgatsby.txt', dtype='str', delimiter=' ', usecols=[0,1,2,3,4,5,6,7,8])
    file = file.reshape(-1)
    random_words = np.random.choice(file, 300)
    return random_words

Builder.load_file('typew.kv')
t = 60
check = 0
global how_many
how_many = 0
def my_callback(screen, dt):
    global t
    global check
    global how_many
    if(t==0):
        t = 60
        check = 0
        screen.ids.timer.text = 'Time: ' + str(t)
        screen.manager.current = 'popup'
        screen.manager.get_screen('popup').get_score()
        return False
    t -= 1
    screen.ids.timer.text = 'Time: ' + str(t)

arr = []
correct = []
usr_input  = []
mistakes = []
class Welcome_screen(Screen):
    pass

class Main_screen(Screen):

    global arr
    global correct
    global usr_input
    #global mistakes
    arr = generate_words()
    text = ''
    input_t = ''
    correct = []
    mistakes = []
    for a in arr:
        text += a + ' '
        
    def generate_words(self):
        self.ids.text_input.text = ''
        arr = generate_words()
        text = ''
        a = ''
        for a in arr:
            a.strip()
            text += a + ' '
        return text
    def start_time(self):
        global check
        global t

        if(check==0):
            check= check+1
            Clock.schedule_interval(partial(my_callback, self), 1)   

    def get_input(self):
        input_t = self.ids.text_input.text
        input_t = input_t.split()
        usr_input = []
        self.correct = []
        global mistakes
        mistakes = []
        self.start_time()
        global how_many
        how_many = 0
        iter = 0
        for i in input_t:
            i.strip()
            usr_input.append(i)
            if (arr[iter]).strip() == i:
                self.correct.append(1)
                how_many += 1
            else:
                self.correct.append(0)
                mistakes.append(i)
            iter += 1
                
    def display_results(self):  
        for a in arr:
            a.strip()
            self.text += a + ' '
        return self.text


class Popup_screen(Screen):
    score = ''
    global how_many
    global mistakes
    def get_score(self): 
        h = ''
        for i in mistakes:
            h = h + i + ' '
        self.ids.results.text = 'Results: ' + str(how_many) + ' WPM'
        self.score = 'Mistakes: ' + h
        self.ids.text_output.text = self.score 
        return self.score
    def get_results(self):
        self.ids.results.text = 'Results: ' + str(how_many) + ' WPM'
        return self.score


class Typing_speed(MDApp):

    def build(self):
        sm = ScreenManager( transition=Factory.FadeTransition())
        screen1 = Welcome_screen(name='welcome_s')
        sm.add_widget(screen1)
        screen2 = Main_screen(name='main_s')
        sm.add_widget(screen2)
        screen3 = Popup_screen(name='popup')
        sm.add_widget(screen3)
        return sm

if __name__ == "__main__":
   
   Typing_speed().run()



