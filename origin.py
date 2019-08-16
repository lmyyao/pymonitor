import asyncio
import psutil
import logging
import time
import requests

import multiprocessing as mp



logging.basicConfig(
        level=logging.DEBUG, 
        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', 
        datefmt='%a, %d %b %Y %H:%M:%S'
)

class Alert(object):
    def __init__(self, handle, value):
        self.handle = handle
        self.value = value

class MonitHandle(object):

    def __init__(self, tag, period, threshold, debug=False):
        self.tag = tag
        self.threshold = threshold
        self.period = period
        self.debug = debug
        
    def run(self):
        v = self.get_metric()
        if v > self.threshold:
            self.alert(v)
        self.sleep()

    def set_debug(self, enabled=True):
        self.debug = enabled

    
    def get_metric(self):
        pass

    def sleep(self):
        time.sleep(self.period)

    def alert(self, v):
        if self.debug:
            logging.debug(f"{self.tag} current value: {v} greater {self.threshold} ")            
        self.do_alert(v)
    
    def do_alert(self):
        pass

class MonitProcess(mp.Process):
    
    def __init__(self, handle, queue):
        mp.Process.__init__(self)
        self.handle = handle
        self.queue = queue

    def run(self):
        self.handle.run()
        self.notify()

    def notify(self):
        self.queue.put(self.handle.tag)

class CPUMonitHandle(MonitHandle):
    
    def get_metric(self):
        return 5
    
    def do_alert(self, v):
        
        requests.post("https://open.feishu.cn/open-apis/bot/hook/e067ec6bd0414db7b4fc62fbcf585e87",
                json={"text": "内存超出"})


class Monitor(object):

    def __init__(self, max_worker=10, queue=None):
        self.max_worker = max_worker
        self.handles = {}
        if queue is None:
            queue = mp.Queue()
        self.queue = queue
        self.processes = {}

    def add_handle(self, handle):
        if isinstance(handle, MonitHandle):
            self.handles[handle.tag] = handle
            return
        raise ValueError("handle class error")

    def wrap_processes(self):
        for tag, handle in self.handles.items():
            self.wrap_process(tag, handle) 

    def wrap_process(self, tag, handle):
        p = MonitProcess(handle, self.queue)
        self.processes[tag] = p
        p.start()
        return p

    def run_forever(self, debug=True):
        self.wrap_processes()

        while True:
            tag = self.queue.get()
            p = self.processes.get(tag)
            p.terminate()
            if debug:
                logging.info(f"tag: {p}")
            self.wrap_process(tag, self.handles.get(tag))


if __name__ == "__main__":
    monitor = Monitor()
    monitor.add_handle(CPUMonitHandle("cpu", 2, 0.5, True))
    monitor.run_forever()

