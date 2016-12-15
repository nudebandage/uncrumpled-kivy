import logging
import webbrowser

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import StringProperty

from kivygui.rules import Style
from kivygui.keybinder import KeyBinder

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
        page = Page()
        # TODO plug system
        page.kb_bind(('ctrl', 'spacebar'), self.app.unc._unc_cmdpane_toggle)
        with open(file, 'r') as f:
            page.text = f.read()

        # th = TabbedPanelHeader()
        # th.content = page
        self.add_widget(page)

    def unc_page_close(self, file):
        logging.info('unc_page_close '+ file)
        with open(file, 'w') as f:
            f.write(self.gui.text)

    def focus_current(self):
        # TODO
        self.content.children[0].focus = True


class Page(KeyBinder, TextInput):
    pass
    # def __init__(self, **kwargs):
        # super().__init__(**kwargs)
    # def keyboard_on_key_down(self, _, keycode, *args):
        # k = self.interesting_keys.get(keycode[0])
        # Let binds be handled by plugins above #TODO
        # if k:
            # super().keyboard_on_key_down(_, keycode, *args)
            # Consume
            # return True

        # Let editor handle as normal insert
        # return False




class EditorApp(App):
    def build(self):
        return UncrumpledEditor()

if __name__ == '__main__':
    EditorApp().run()
