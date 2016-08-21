from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import BooleanProperty

from kivygui.rules import Style


class CommandPane(FloatLayout, Style):
    visible = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # def key_action(self, _, __, keycode, keysym, modifiers):
        # print('rip')
        # if modifiers == ['ctrl']:
            # if keysym and keysym == ' ':
                # print('hi')
                # self.toggle_pane()

    def toggle(self):
        if self.visible:
            self.visible = False
        else:
            self.visible = True

    # def open_pane(self):

    # def close_pane(self):


class CmdPane(App):
    def build(self):
        return CommandPane()

if __name__ == '__main__':
    CmdPane().run()
