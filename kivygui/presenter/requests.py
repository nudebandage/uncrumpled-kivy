'''
    send requests to the uncrumpled presenter

    Kivy async support is pretty new so i cannot use the asyncio.coroutine etc
'''
import logging
import json

from async_gui.toolkits.kivy import KivyEngine
from async_gui.engine import Task

from uncrumpled.presenter import requests

engine = KivyEngine()

class Requests():
    # Delegate the function from uncrumpled to self._unc_

    def do(self, func, **kwargs):
        print('request sent -> ', func)
        reqfunc = eval('requests.{}'.format(func))
        response = reqfunc(self._unc_app, **kwargs)
        for resp_func in response:
            try:
                eval('self._unc_{}'.format(resp_func))
            except Exception as err: # JFT
                logging.exception(resp_func+' '+ err)
                raise

    @engine.async
    def async_request(self, func, **kwargs):
        yield Task(lambda: self.do(func, **kwargs))

    def req_cmdpane_search(self, query):
        self.async_request('cmdpane_search', query=query)

    def req_cmdpane_item_open(self, item):
        self.async_request('cmdpane_item_open', item=item)

    def req_ui_init(self):
        self.async_request('ui_init')

    def req_book_create(self, profile, book, hotkey, active_profile, **kwargs):
        try:
            assert(type(hotkey) == list)
        except AssertionError:
            import pdb;pdb.set_trace()
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
