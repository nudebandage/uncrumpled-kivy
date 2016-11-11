from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import BooleanProperty

from kivygui.rules import Style


class CommandPane(FloatLayout, Style):
    visible = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def toggle(self):
        '''
        toggle the cmd pane open or close
        '''
        if self.visible:
            self.visible = False
        else:
            self.visible = True

    def search(self):
        '''
        query the uncrumpled core for results from a search
        and display them
        '''
        # results come back as heading and text..
        pass

    def open_search_item(self):
        '''
        the user wants to do something with a search result..
        get the result and query the core for what to do
        '''
        pass


class CmdPane(App):
    def build(self):
        return CommandPane()

if __name__ == '__main__':
    CmdPane().run()
