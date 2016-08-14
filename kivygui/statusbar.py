from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from rules import Style

class StatusBar(FloatLayout, Style):
    pass

class StatusBarApp(App):
    def build(self):
        return CommandPane()

if __name__ == '__main__':
    StatusApp().run()
