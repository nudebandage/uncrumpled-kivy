'''
    send requests to the uncrumpled presenter

    Kivy async support is pretty new so i cannot use the asyncio.coroutine etc
'''
from uncrumpled.presenter import requests


class Requests():
    def async_request(self, func, **kwargs):
        def _(self, **kwargs):
            response = eval('requests.{}(self, self.core, **kwargs)'.format(func))
            if isinstance(response, (list, tuple)):
                for resp_func in response:
                    eval('self.' + resp_func)
            else:
                eval('self.' + response)
        self.ev.run_until_complete(
                self.ev.run_in_executor(None, _, self, **kwargs))


    def ui_init(self):
        self.async_request(self, )
        pass

    def profile_create(self, profile):
        self.async_request('profile_create', profile=profile)
