
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from kivygui.rules import Style


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))

class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        # self.data = [{'text': str(x)} for x in range(40)]


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
            self.searchbox.focus = True

    # @rate_limited(1) TODO this is already fucking up because of async.... wait till async is not bugging..
    def search(self):
        '''
        query the uncrumpled core for results from a search
        and display them
        '''
        query = self.searchbox.text
        if query:
            # This request results in a call to display_search_results
            self.root.req_cmdpane_search(query)

    def display_search_results(self, headings, bodies):
        bodies = map(lambda x: x if x else '', bodies)
        self.recycleview.data = [{'text': '{}\n{}'.format(h, b)}
                                    for h, b in zip(headings, bodies)]

    def open_search_item(self):
        '''
        the user wants to do something with a search result..
        get the result and query the core for what to do
        '''
        pass

    def do(self, *args):
        print('fdsaf')


    def ui_build(self, ui):
        pass

# class SearchBox(TextInput):

    # def __init__(self, **kwargs):
        # super().__init__(**kwargs)

    # def _focus(self):
        # print('1')


class CmdPane(App):
    def build(self):
        return CommandPane()

if __name__ == '__main__':
    CmdPane().run()
