'''
   The main window for uncrumpled, this is the entry point for the gui

   We Marry some Requests and Responses, as well as sytem wide hotkeys.
   Also handling some window methods such as open close etc
'''

import logging
import queue
import json
from contextlib import suppress

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


class Keybinder():
    def setup_config(self):
        self._keyboard = self.window.request_keyboard(self._keyboard_closed, self)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _run_bind(self, callback_string):
        # Callback is meant to be handled by the gui...
        callback = callback_string.split('(')[0]
        if hasattr(self, 'unc_' + callback):
            eval('self.unc_' + callback_string)
        # The callback must be meant for the core...
        else:
            eval('self.req_' + callback_string)

    def _make_hkstring(self, keysym, modifiers):
        with suppress(ValueError):
            keysym = int(keysym)
        hotkey = [keysym, *modifiers]
        return json.dumps(hotkey)

    def handler_on_key_down(self, _, keycode, keysym, modifiers):
        # import pdb;pdb.set_trace()
        hotkey = self._make_hkstring(keysym, modifiers)
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

    # This is run in another thread, which async code doesn't play well with.
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

    def unc_bind_add(self, hk, event_type, command, command_kwargs):
        assert event_type in self.supported_bind_handlers
        # Setup the bind handler if first time
        if event_type not in self.active_bind_handlers:
            handler = 'self.handler_' + event_type
            eval('self._keyboard.bind({}={})'.format(event_type, handler))
            self.active_bind_handlers.append(event_type)
        command_str = '{cmd}(**{kwargs})'.format(cmd=command, kwargs=command_kwargs)
        self.active_binds.setdefault(event_type, {})[hk] = [command_str]


    def unc_window_show(self):
        logging.info('unc_window_show')
        self.window.show()

    def unc_window_hide(self): #TODO
        '''hide the window, also tell uncrumpled all the pages we closed'''
        logging.info('unc_window_hide')
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
        '''call to start the gui (only used by the backend)'''
        self.unc_app = unc_app
        self.ev = KivyEventLoop(self)
        # self.ev.set_debug(True)
        self.ev.mainloop()

    def build(self):
        root = MyScreenManager()
        Clock.schedule_once(lambda e: root.remove_loadscreen(), 4)
        # If we are are being run by the backend
        if hasattr(self, 'ev'):
            # Find the widget handling our requests/responses and call ui_init
            for screen in root.screens:
                if screen.name == 'uncrumpled':
                    screen.ev = self.ev
                    screen._unc_app = self.unc_app
                    # screen.kivy_app = self
                    Clock.schedule_once(lambda e: screen.setup_config(), 0)
                    screen.req_ui_init() # TODO ASYNC THIS
                    break
        return root


if __name__ == '__main__':
    ToplevelApp().run()
