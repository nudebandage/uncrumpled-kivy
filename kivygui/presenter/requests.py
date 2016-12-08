'''
    send requests to the uncrumpled presenter

    Kivy async support is pretty new so i cannot use the asyncio.coroutine etc
'''
import logging

from uncrumpled.presenter import requests


class Requests():
    # Delegate the function from uncrumpled to self._unc_
    def async_request(self, func, **kwargs):
        def _(self, **kwargs):
            print('request sent -> ', func)
            reqfunc = eval('requests.{}'.format(func))
            response = reqfunc(self._unc_app, **kwargs)
            for resp_func in response:
                try:
                    # if 'ui' in resp_func:
                        # import pdb;pdb.set_trace()
                    # if 'gotten' in resp_func:
                        # import pdb;pdb.set_trace()
                    eval('self._unc_{}'.format(resp_func))
                except Exception as err: # JFT
                    logging.critical(resp_func+' '+ err)
        self.ev.run_until_complete(
                self.ev.run_in_executor(None, _, self, **kwargs))

    def req_cmdpane_search(self, query):
        self.async_request('cmdpane_search', query=query)

    def req_cmdpane_item_open(self, item):
        self.async_request('cmdpane_item_open', item=item)

    def req_ui_init(self):
        self.async_request('ui_init')

    def req_book_create(self, profile, book, hotkey, active_profile, **kwargs):
        self.async_request('book_create', profile=profile,
                                          book=book,
                                          hotkey=hotkey,
                                          active_profile=active_profile,
                                          **kwargs)

    def req_profile_create(self, profile):
        self.async_request('profile_create', profile=profile,)

    def req_hotkey_pressed(self, profile, program, hotkey):
        self.async_request('hotkey_pressed', profile=profile, program=program,
                                             hotkey=hotkey)
    def req_system_get(self):
        self.async_request('system_get')
