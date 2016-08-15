
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import BooleanProperty

from kivygui.rules import Style


class SplashPage(FloatLayout, Style):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class SplashApp(App):
    def build(self):
        return SplashPage()

if __name__ == '__main__':
    SplashApp().run()
