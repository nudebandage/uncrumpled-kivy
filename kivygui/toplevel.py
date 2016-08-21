'''
   The main window for uncrumpled

   We Marry some Requests and Responses, as well as sytem wide hotkeys.
   Also handling some window methods such as open close etc
'''

import logging

from system_hotkey import SystemHotkey
import peasoup

from kivy.app import App
from kivy.base import KivyEventLoop
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition

from kivygui.presenter import Requests
from kivygui.presenter import Responses
# Have to import all the components used for kv lang to use
from kivygui.editor import UncrumpledEditor
from kivygui.cmdpane import CommandPane
from kivygui.workbench import Workbench
from kivygui.statusbar import StatusBar
from kivygui.splash import SplashPage
from kivygui import settings
from kivygui.rules import Style
from kivygui._config import _Config


class MyScreenManager(ScreenManager):
    def remove_loadscreen(self):
        self.transition = FadeTransition()
        self.current = self.current = 'uncrumpled'


class UncrumpledWindow(Screen, Style, Responses, Requests, _Config):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = Window
        self.bind(on_touch_down=self.touch_handler)

    def unc_show_window(self):
        self.window.show()

    def unc_hide_window(self):
        self.window.hide()

    def touch_handler(self, _, touch): # JFT
        if self.ids.commandpane.collide_point(*touch.pos):
            self.ids.commandpane.toggle()
            # touch.grab(self.ids.commandpane)
            return True
        if self.ids.workbench.collide_point(*touch.pos):
            self.ids.workbench.toggle()
            return True
        self.ids.workbench.visible = 1
        self.ids.commandpane.visible = 1


class ToplevelApp(App):
    def start(self, unc_app):
        '''call to start the gui'''
        self.hk = SystemHotkey(consumer=self.hotkey_consumer,
                               check_queue_interval=0.001)
        self.unc_app = unc_app
        self.ev = KivyEventLoop(self)
        # self.ev.set_debug(True)
        self.ev.mainloop()

    def hotkey_consumer(self, event, hotkey, args):
        program, pid, = peasoup.process_exists() # TODO rename this func
        profile = self.active_profile
        self.req_hotkey_pressed(profile, program, hotkey)

    def build(self):
        root = MyScreenManager()
        Clock.schedule_once(lambda e: root.remove_loadscreen(), 4)
        # find the widget handling our requests/responses and call ui_init
        if hasattr(self, 'ev'):
            for screen in root.screens:
                if screen.name == 'uncrumpled':
                    screen.ev = self.ev
                    screen._unc_app = self.unc_app
                    screen.kivy_app = self
                    Clock.schedule_once(lambda e: screen.setup_config(), 4)
                    screen.req_ui_init() # TODO ASYNC THIS
        return root


if __name__ == '__main__':
    ToplevelApp().run()
