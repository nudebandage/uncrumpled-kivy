'''
    resposnes from uncrumpled invoke methods defined here.
    if we can, delegate to a widget that handles the response
    some response types don't have widget and so are defined here
    e.g bind_add
'''
import logging


class Responses():
    '''run the responses from uncrumpled'''
    def _unc_status_update(self, msg, code):
        self.ids.statusbar.unc_update_status(msg, code)

    def _unc_show_window(self):
        self.unc_show_window()

    def _unc_welcome_screen(self):
        logging.warning('unc_welcome_screen not implemented')
        # self.unc_welcome_screen()

    def _unc_page_load(self, file):
        self.ids.editor.unc_page_load(file)

    def _unc_page_close(self):
        self.ids.editor.unc_page_close(file)

    def _unc_system_hotkey_register(self, hotkey):
        logging.info('binding hotkeyL ' +hotkey)
        self.kivy_app.hk.register(hotkey)

    def _unc_system_hotkey_unregister(self, hotkey):
        self.kivy_app.hk.unregister(hotkey)

    def _unc_profile_set_active(self, profile):
        logging.warning('profile_set_active')
        # self.kivy_app.pf.set_active(profile)


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

