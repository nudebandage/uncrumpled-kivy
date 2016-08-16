'''
   The main window for uncrumpled
'''
import os
from kivy.app import App
from kivy.base import KivyEventLoop
from kivy.base import Builder
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition

# Have to import all the components used for kv lang to use
from kivygui.editor import UncrumpledEditor
from kivygui.cmdpane import CommandPane
from kivygui.workbench import Workbench
from kivygui.statusbar import StatusBar
from kivygui.splash import SplashPage
from kivygui.rules import Style
from kivygui.globals import EV, CORE

from kivygui.presenter import Requests
from kivygui.presenter import Responses

from kivygui import settings


class MyScreenManager(ScreenManager):
    pass

class UncrumpledWindow(Screen, Style, Responses, Requests):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Window.bind(on_key_down=self.key_down_handler)
        # Window.bind(on_touch_down=self.touch_handler)
        # self.ids.commandpane.bind(on_touch_down=self.touch_handler)
        self.bind(on_touch_down=self.touch_handler)
        global EV, CORE
        self.ev = EV
        self.core = CORE

    def touch_handler(self, _, touch):
        if self.ids.commandpane.collide_point(*touch.pos):
            self.ids.commandpane.toggle()
            # touch.grab(self.ids.commandpane)
            return True
        if self.ids.workbench.collide_point(*touch.pos):
            self.ids.workbench.toggle()
            return True
        self.ids.workbench.visible = 1
        self.ids.commandpane.visible = 1

    def key_down_handler(_, __, keycode, keysym, modifiers, system):
        '''
        checks if the key has a callback bound to it and
        runs it
        '''
        import pdb;pdb.set_trace()



class ToplevelApp(App):

    def start(self, core):
        ''' Passing references for the event loop and core'''
        global EV, CORE
        ev = KivyEventLoop(self)
        EV = ev
        CORE = core
        Requests.ui_init(core)
        ev.set_debug(True)
        ev.mainloop()

    def finish_load(self):
        self.root.transition = FadeTransition()
        self.root.current = self.root.current = 'uncrumpled'

    def build(self):
        root = self.root
        Clock.schedule_once(lambda e: self.finish_load(), 2)
        return MyScreenManager()


if __name__ == '__main__':
    ToplevelApp().run()


