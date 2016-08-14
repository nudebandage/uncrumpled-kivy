from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import BooleanProperty

from kivygui.rules import Style


class Workbench(FloatLayout, Style):
    visible = BooleanProperty(True)
    def __init__(self, **kwargs):
        super().__init__()

class WorkbenchApp(App):
    def build(self):
        return Workbench()

if __name__ == '__main__':
    WorkbenchApp().run()