import requests
import datetime


class BaseAlert(object):
    def __init__(self, handle, value):
        self.handle = handle
        self.value = value

    def do_alert(self):
        pass

    def message(self):
        return f'{datetime.datetime.now()} {self.handle.tag} current value is: {self.value} greater threshold value: {self.handle.threshold}'


class LackAlert(BaseAlert):
    LackWebHook = "https://open.feishu.cn/open-apis/bot/hook/"
    _hook_id = None

    @classmethod
    def set_hook_id(cls, hook_id):
        cls._hook_id = hook_id

    def do_alert(self):
        requests.post(f'{self.LackWebHook}{self._hook_id}', json={"text": self.message()})

