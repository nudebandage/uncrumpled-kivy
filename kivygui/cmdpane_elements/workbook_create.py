from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from kivygui.keybinder import KeyBinder

import pdb

Y = 40

class CmdPaneElement():
    def clear_values(self):
        raise NotImplementedError

    def first_focusable(self, x):
        raise NotImplementedError


class WorkbookCreate(BoxLayout, CmdPaneElement):
    def clear_values(self):
        pass

    def insert_values(self, **kwargs):
        '''insert the values into fields for initialization'''
        pass


class SmartText(KeyBinder, TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kb_bind(('tab',), self.tab_pressed)
        self.kb_bind(('shift', 'tab',), self.shift_tab_pressed)

    def tab_pressed(self):
        self.focus_next.focus = True

    def shift_tab_pressed(self):
        self.focus_previous.focus = True


def workbook_create():
    '''
    return a KivyWidget to be added to the cmdpane
    '''
    layout = WorkbookCreate(orientation='vertical',
                            spacing=5)
    # layout.size_hint_y = None
    # layout.height = 700
    # layout.pos_hint = {'top':1}
    # layout.pos_hint_y = None
    label_args = {}
    # label_args = {'height': Y}
    # label_args = {'size_hint_y': None, 'height': Y}
    # label_args = {'pos_hint_y': None, 'size_hint_y': None, 'pos': layout.pos,'height': Y}
    name = SmartText(id='name')
    hotkey = SmartText(id='hotkey')
    profile = SmartText(id='profile')
    name.focus_next = hotkey
    hotkey.focus_next = profile
    profile.focus_next = name
    layout.add_widget(Label(text='Create Workbook', **label_args))
    layout.add_widget(Label(text='Name', **label_args))
    layout.add_widget(name)
    layout.add_widget(Label(text='Hotkey', **label_args))
    layout.add_widget(hotkey)
    layout.add_widget(Label(text='Profile', **label_args))
    layout.add_widget(profile)
    layout.add_widget(Button(text='Create', on_press = lambda x:pdb.set_trace(), **label_args))

    layout.first_focusable = lambda: name
    layout.last_focusable = lambda: profile
    return layout


if __name__ == '__main__':
    # EXAMPLE

    from kivy.app import App

    class MyApp(App):
        def build(self):
            return workbook_create()

    MyApp().run()



