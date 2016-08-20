'''
   The main window for uncrumpled
'''

import os
import logging

from kivy.app import App
from kivy.base import KivyEventLoop
from kivy.base import Builder
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.factory import Factory

# Have to import all the components used for kv lang to use
from kivygui.editor import UncrumpledEditor
from kivygui.cmdpane import CommandPane
from kivygui.workbench import Workbench
from kivygui.statusbar import StatusBar
from kivygui.splash import SplashPage
from kivygui.rules import Style

from kivygui.presenter import Requests
from kivygui.presenter import Responses
from kivygui import settings


class MyScreenManager(ScreenManager):
    def remove_loadscreen(self):
        self.transition = FadeTransition()
        self.current = self.current = 'uncrumpled'


class UncrumpledWindow(Screen, Style, Responses, Requests):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = Window
        self.bind(on_touch_down=self.touch_handler)

    def on_root(self):
        import pdb;pdb.set_trace()

    def unc_show_window(self):
        self.window.show()

    def unc_hide_window(self):
        self.window.hide()

    def unc_welcome_screen(self):
        logging.warning('unc_welcome_screen not implemented')
        pass

    def touch_handler(self, _, touch):
        import pdb;pdb.set_trace()
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

    def start(self, unc_app):
        '''call to start the gui'''
        self.unc_app = unc_app
        self.ev = KivyEventLoop(self)
        # self.ev.set_debug(True)
        self.ev.mainloop()

    def build(self):
        root = MyScreenManager()
        Clock.schedule_once(lambda e: root.remove_loadscreen(), 4)
        # find the widget handling our requests/responses and call ui_init
        if hasattr(self, 'ev'):
            for screen in root.screens:
                if screen.name == 'uncrumpled':
                    self.main_window = screen # Used uncrumpled/main
                    screen.ev = self.ev
                    screen._unc_app = self.unc_app
                    screen.req_ui_init() # TODO ASYNC THIS
        return root


if __name__ == '__main__':
    ToplevelApp().run()
