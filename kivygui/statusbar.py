from kivy.app import App
from kivy.uix.floatlayout import FloatLayout

from kivygui.rules import Style

class StatusBar(FloatLayout, Style):
    def update_status(self, msg, code):
        import pdb;pdb.set_trace()
        self.ids.msg.text = msg
    pass

class StatusBarApp(App):
    def build(self):
        return StatusBar()

if __name__ == '__main__':
    StatusBarApp().run()
