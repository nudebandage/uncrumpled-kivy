'''
    resposnes from uncrumpled invoke methods defined here.
    if we can, delegate to a widget that handles the response
    some response types don't have widget and so are defined here
    e.g bind_add
'''
import logging
from pprint import pprint
import json


def _run_bind(unc, callback_string):
    def _():
        import pdb;pdb.set_trace()
        callback = callback_string.split('(')[0]
        if hasattr(unc, '_unc_' + callback):
            eval('unc._unc_' + callback_string)
        # The callback must be meant for the core...
        else:
            eval('unc.req_' + callback_string)
    return _


class Responses():
    '''run the responses from uncrumpled'''
    def _unc_bind_add(self, hotkey, event_type, command, command_kwargs):
        hotkey = json.loads(hotkey)
        assert event_type in self.supported_bind_handlers
        command_str = '{cmd}(**{kwargs})'.format(cmd=command,
                                                 kwargs=command_kwargs)
        # self.kb_bind((2,), lambda: print(2))
        # self.kb_bind(('2',), lambda : print(1))
        self.kb_bind(hotkey, _run_bind(self, command_str))

    def _unc_bind_remove(self, hotkey, event_type, command):
        import pdb;pdb.set_trace()

    def _unc_cmdpane_search_results(self, headings, bodies):
        self.ids.commandpane.display_search_results(headings, bodies)

    def _unc_cmdpane_ui_build(self, ui):
        self.ids.commandpane.ui_build(ui)

    def _unc_cmdpane_toggle(self):
        self.ids.commandpane.toggle()

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

    def _unc_profile_set_active(self, profile):
        logging.warning('profile_set_active')
        self.active_profile = profile
        # self.kivy_app.pf.set_active(profile)

    def _unc_system_gotten(self, system):
        import json
        system = json.loads(system)
        pprint(system)
