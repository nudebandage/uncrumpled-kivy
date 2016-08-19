'''
    resposnes from uncrumpled invoke methods defined here.
    if we can, delegate to a widget that handles the response
    some response types don't have widget and so are defined here
    e.g bind_add
'''


class Responses():
    '''run the responses from uncrumpled'''
    def _unc_status_update(self, msg, code):
        self.ids.statusbar.unc_update_status(msg, code)

    def _unc_show_window(self):
        self.unc_show_window()

    def _unc_welcome_screen(self):
        self.unc_welcome_screen()


def key_down_handler(_, __, keycode, keysym, modifiers, system):
    '''
    checks if the key has a callback bound to it and
    runs it
    '''
    get_hkstring(keysym, modifiers)
    callbacks =  system['binds']['key_down'].get(hkstring)
    for cb in callbacks:
        if cb not in BINDS:
            cb()


    # def key_action(self, _, __, keycode, keysym, modifiers):
        # if modifiers == ['ctrl']:
            # if keysym and keysym == ' ':
                # self.toggle_pane()
