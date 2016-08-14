'''
   The main window for uncrumpled
'''
# https://gist.github.com/tshirtman/504cf579b5d2aafb0ca1c679910307ed
# https://gist.github.com/tshirtman/e481319b91483278203fe6c1f024c65a
from kivy.app import App
from kivy.base import KivyEventLoop
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

# Have to import all the components used for kv lang to use
# from unc import ui_connect
from kivygui.editor import UncrumpledEditor
from kivygui.cmdpane import CommandPane
from kivygui.workbench import Workbench
from kivygui.rules import Style

# from kivygui.api import CommandsMixIn

class CommandsMixIn():
    def toggle(self):
        pass

def key_down_handler(_, __, keycode, keysym, modifiers, system):
    '''
    checks if the key has a callback bound to it and
    runs it
    '''
    get_hkstring(keysym, modifiers)
    callbacks =  system['binds']['key_down'].get(hkstring)
    for cb in callbacks:
        if cb not in BINDS:
            cb()

class UncrumpledWindow(FloatLayout, Style):
    pass

class ToplevelApp(App, CommandsMixIn):

    def start(self):
        # self.core = core
        self.ev = KivyEventLoop(self)
        self.ev.set_debug(True)
        self.ev.mainloop()

    def build(self):
        return UncrumpledWindow()

    # def forever_and_ever(self, function):
        # '''
        # run a function asynchronously
        # '''
        # Clock.schedule_once(lambda e: self.ev.run_in_executor(None, function), 100)

    # def key_action(self, _, __, keycode, keysym, modifiers):
        # if modifiers == ['ctrl']:
            # if keysym and keysym == ' ':
                # self.toggle_pane()





if __name__ == '__main__':
    ToplevelApp().run()
