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
        assert event_type in self.supported_bind_handlers
        # Setup the bind handler if first time
        if event_type not in self.active_bind_handlers:
            handler = 'self.handler_' + event_type
            eval('self._keyboard.bind({}={})'.format(event_type, handler))
            self.active_bind_handlers.append(event_type)
        command_str = '{cmd}(**{kwargs})'.format(cmd=command, kwargs=command_kwargs)
        self.active_binds.setdefault(event_type, {})[hotkey] = [command_str]

    def _unc_bind_remove(self, hotkey, event_type, command):
        pass

    def _unc_cmdpane_toggle(self):
        self.ids.commandpane.toggle()
        # import pdb;pdb.set_trace()

    def _unc_status_update(self, msg, code):
        self.ids.statusbar.unc_update_status(msg, code)

    def _unc_window_show(self):
        logging.info('unc_window_show')
        self.window.show()

    def _unc_window_hide(self): #TODO
        '''hide the window, also tell uncrumpled all the pages we closed'''
        logging.info('unc_window_hide')
        self.window.hide()

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

