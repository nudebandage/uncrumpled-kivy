'''
   The main window for uncrumpled
'''

from kivy.app import App
from kivy.base import KivyEventLoop
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty

# Have to import all the components used for kv lang to use
from kivygui.editor import UncrumpledEditor
from kivygui.cmdpane import CommandPane
from kivygui.workbench import Workbench
from kivygui.statusbar import StatusBar
from kivygui.rules import Style
from kivygui.globals import EV, CORE

from kivygui.presenter import Requests
from kivygui.presenter import Responses


class UncrumpledWindow(FloatLayout, Style, Responses, Requests):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        global EV, CORE
        self.ev = EV
        self.core = CORE


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

    def build(self):
        return UncrumpledWindow()


if __name__ == '__main__':
    ToplevelApp().run()
