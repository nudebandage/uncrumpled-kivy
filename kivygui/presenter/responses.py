'''
    resposnes from uncrumpled invoke methods defined here.
    if we can, delegate to a widget that handles the response
    some response types don't have widget and so are defined here
    e.g bind_add
'''
import logging
from pprint import pprint


class Responses():
    '''run the responses from uncrumpled'''
    def _unc_bind_add(self, hotkey, event_type, command, command_kwargs):
        self.unc_bind_add(hotkey, event_type, command, command_kwargs)

    def _unc_bind_remove(self, hotkey, event_type, command):
        pass

    def _unc_status_update(self, msg, code):
        self.ids.statusbar.unc_update_status(msg, code)

    def _unc_window_show(self):
        self.unc_window_show()

    def _unc_window_hide(self):
        self.unc_window_hide()

    def _unc_welcome_screen(self):
        logging.warning('unc_welcome_screen')
        # self.unc_welcome_screen()

    def _unc_page_load(self, file):
        self.ids.editor.unc_page_load(file)

    def _unc_page_close(self, file):
        self.ids.editor.unc_page_close(file)

    def _unc_system_hotkey_register(self, hotkey):
        # TODO handle a failed register...
        logging.info('binding hotkey ' + str(hotkey))
        self.hk.register(hotkey)

    def _unc_system_hotkey_unregister(self, hotkey):
        self.hk.unregister(hotkey)

    def _unc_profile_set_active(self, profile):
        logging.warning('profile_set_active')
        self.active_profile = profile
        # self.kivy_app.pf.set_active(profile)

    def _unc_system_gotten(self, system):
        pprint(system)


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

