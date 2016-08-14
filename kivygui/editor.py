from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel

from kivygui.rules import Style

class UncrumpledEditor(TabbedPanel):
    pass

class EditorApp(App):
    def build(self):
        return UncrumpledEditor()

if __name__ == '__main__':
    EditorApp().run()
