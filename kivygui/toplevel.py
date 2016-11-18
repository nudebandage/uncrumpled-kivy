'''
   The main window for uncrumpled, this is the entry point for the gui

   We Marry some Requests and Responses, as well as sytem wide hotkeys.
   Also handling some window methods such as open close etc
'''

import logging
import queue
import json
import os
from contextlib import suppress

from system_hotkey import SystemHotkey
import peasoup

from kivy.app import App
from kivy.base import KivyEventLoop
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition

from kivygui.presenter import Requests
from kivygui.presenter import Responses
# Have to import all the components used for kv files to use
from kivygui.editor import UncrumpledEditor
from kivygui.cmdpane import CommandPane
from kivygui.workbench import Workbench
from kivygui.statusbar import StatusBar
from kivygui.splash import SplashPage
from kivygui import settings
from kivygui.rules import Style


class Keybinder():
    def setup_keybind(self, window):
        self._keyboard = window.request_keyboard(self._keyboard_closed, self)

    def _keyboard_closed(self):
        # TODO somehow need to reopen this
        pass
        self._keyboard.unbind(on_key_down=self.handler_on_key_down)
        self._keyboard = None

    def _run_bind(self, callback_string):
        # Callback is meant to be handled by the gui...
        callback = callback_string.split('(')[0]
        if hasattr(self, '_unc_' + callback):
            eval('self._unc_' + callback_string)
        # The callback must be meant for the core...
        else:
            eval('self.req_' + callback_string)

    def _make_hkstring(self, keysym, modifiers):
        with suppress(ValueError):
            keysym = int(keysym)
        hotkey = [keysym, *modifiers]
        return json.dumps(hotkey)

    def handler_on_key_down(self, _, keycode, keysym, modifiers):
        hotkey = self._make_hkstring(keycode[1], modifiers)
        commands = self.active_binds['on_key_down'].get(hotkey)
        with suppress(TypeError):
            for cb in commands:
                self._run_bind(cb)


class MyScreenManager(ScreenManager):
    def remove_loadscreen(self):
        self.transition = FadeTransition()
        self.current = self.current = 'uncrumpled'


class UncrumpledWindow(Screen, Style, Responses, Requests, Keybinder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = Window
        self.setup_keybind(self.window)
        self.hk = SystemHotkey(consumer=self.sys_hotkey_handler,
                               check_queue_interval=0.001)
        self.hk.register(['f7'], self.req_system_get) # JFT
        self.queue = queue.Queue()
        Clock.schedule_interval(lambda e: self.check_queue(), 0.01)
        self.supported_bind_handlers = ('on_key_down',)
        self.active_bind_handlers = []
        self.active_binds = {} # {event_type: {hk [cb1, cb2]}]}

    def check_queue(self):
        try:
            func = self.queue.get(block=False)
        except queue.Empty:
            pass
        else:
            try:
                func()
            except Exception as err:
                # An error happend over on the backend :(
                import pdb;pdb.set_trace()

    def run_in_main(self, func):
        self.queue.put(func)

    # This is run in another thread, errors here do not get propogated due to async..
    def sys_hotkey_handler(self, event, hotkey, args):
        self.active_profile = 'default'
        program, pid, = peasoup.process_exists() # TODO rename this func
        profile = self.active_profile
        # Mainly for testing, a hotkey has bound it's own callback
        if args[0]:
            self.run_in_main(args[0][0])
        else:
            self.run_in_main(lambda: self.req_hotkey_pressed(
                                        profile, program, hotkey))

    # def touch_handler(self, _, touch): # JFT
        # if self.ids.commandpane.collide_point(*touch.pos):
            # self.ids.commandpane.toggle()
            # touch.grab(self.ids.commandpane)
            # return True
        # if self.ids.workbench.collide_point(*touch.pos):
            # self.ids.workbench.toggle()
            # return True
        # self.ids.workbench.visible = 1
        # self.ids.commandpane.visible = 1


class ToplevelApp(App):
    def start(self, unc_app):
        '''call to start the gui (only used by the backend)'''
        self.unc_app = unc_app
        self.ev = KivyEventLoop(self)
        if self.unc_app.DEVELOPING:
            # Has some performance penalties
            self.ev.set_debug(True)
        self.ev.mainloop()

    def build(self):
        root = MyScreenManager()
        Clock.schedule_once(lambda e: root.remove_loadscreen(), 4)
        # Find the widget handling our requests/responses and call ui_init
        for screen in root.screens:
            if screen.name == 'uncrumpled':
                screen.ev = self.ev
                # Backend/Core
                screen._unc_app = self.unc_app
                # Main Uncrumpled Screen
                self.unc = screen
                # screen.kivy_app = self
                screen.req_ui_init() # TODO ASYNC THIS
                break
        return root


if __name__ == '__main__':

    class TestSync(ToplevelApp):
        def build(self):
            path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'toplevel.kv'))
            # Required becaues this class name != name of kv file
            Builder.load_file(path)
            root = MyScreenManager()
            Clock.schedule_once(lambda e: root.remove_loadscreen(), 4)
            return root

    class TestAsync(TestSync):
        def start(self):
            logging.basicConfig(level=logging.DEBUG)
            self.ev = KivyEventLoop(self)
            self.ev.set_debug(True)
            self.ev.mainloop()

    # TestSync().run()
    TestAsync().start()
