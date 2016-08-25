import logging
import webbrowser

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.label import Label
from kivy.properties import StringProperty
from kivygui.rules import Style

_welcome='''
        [size=70][font=Inconsolata]uncrumpled[/font][/size]

        Welcome to the latest version of Uncrumpled.
        If you are new please check out the Online `Docs`
        You can also use the `Command Pane` for quick
        help on anything in Uncrumpled `Ctrl + Space`

        If you run into any problems please report them on `Github`!
        '''

class MultiLineLabel(Label):
    def __init__(self, **kwargs):
        super(MultiLineLabel, self).__init__( **kwargs)
        self.markup = True
        self.text_size = self.size
        self.bind(size= self.on_size)
        self.bind(text= self.on_text_changed)
        self.size_hint_y = None # Not needed here

    def on_size(self, widget, size):
        self.text_size = size[0], None
        self.texture_update()
        if self.size_hint_y == None and self.size_hint_x != None:
            self.height = max(self.texture_size[1], self.line_height)
        elif self.size_hint_x == None and self.size_hint_y != None:
            self.width  = self.texture_size[0]

    def on_text_changed(self, widget, text):
        self.on_size(self, self.size)


class UncrumpledEditor(TabbedPanel):
    file = None
    gui = None
    # welcome_text = StringProperty(_welcome)
    # def open_link(link):
        # webbrowser.open(link)
    def unc_page_load(self, file):
        # TODO FOCUS WINDOW, SEEK 0, 0
        logging.info('unc_page_load '+ file)
        self.file = file
        self.gui = self.content.children[0]
        with open(file, 'r') as f:
            self.gui.text = f.read()

    def unc_page_close(self, file):
        logging.info('unc_page_close '+ file)
        with open(file, 'w') as f:
            f.write(self.gui.text)


class EditorApp(App):
    def build(self):
        return UncrumpledEditor()

if __name__ == '__main__':
    EditorApp().run()
