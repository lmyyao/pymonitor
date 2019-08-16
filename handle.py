import psutil
import logging
import time

logging.basicConfig(
    level=logging.DEBUG,
    format=
    '%(asctime)s %(filename)s %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S')



class BaseHandle(object):
    def __init__(self,
                 tag,
                 period,
                 threshold,
                 AlertHandleClass=None,
                 debug=False, continuous_alert=5):
        self.tag = tag
        self.threshold = threshold
        self.period = period
        self.debug = debug
        if AlertHandleClass is None:
            self.alert_class = BaseAlert
        else:
            self.alert_class = AlertHandleClass
        self.continuous_alert = continuous_alert
        self.alert_count = 0

    def run(self):
        v = self.get_metric()
        if v > self.threshold:
            if self.alert_count < self.continuous_alert:
                self.alert(v)
            else:
                logging.debug(f"alert_count: {self.alert_count}")
            self.alert_count += 1
        else:
            if self.debug:
                logging.debug(f"{self.tag} current value: {v} less {self.threshold} ")
            self.alert_count = 0

        self.sleep()

    def set_debug(self, enabled=True):
        self.debug = enabled

    def get_metric(self):
        pass

    def sleep(self):
        time.sleep(self.period)

    def alert(self, v):
        if self.debug:
            logging.debug(
                f"{self.tag} current value: {v} greater {self.threshold} ")
        self.do_alert(v)

    def do_alert(self, v):
        alert = self.alert_class(self, v)
        alert.do_alert()

class CPUMonitHandle(BaseHandle):
    def get_metric(self):
        return psutil.cpu_percent(1)

class DiskMonitHandle(BaseHandle):

    def get_metric(self):
        return psutil.disk_usage("/").percent

