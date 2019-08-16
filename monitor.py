import logging
import multiprocessing as mp
import concurrent.futures
from .handle import BaseHandle

logging.basicConfig(
    level=logging.DEBUG,
    format=
    '%(asctime)s %(filename)s %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S')

class Monitor(object):
    def __init__(self, max_worker=10, queue=None):
        self.handles = {}
        if queue is None:
            queue = mp.Queue()
        self.queue = queue
        self.processes = {}
        self.executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_worker)

    def add_handle(self, handle):
        if isinstance(handle, BaseHandle):
            self.handles[handle.tag] = handle
            return
        raise ValueError("handle class error")

    def _wrap_handle(self, handle, queue):
        handle.run()
        queue.put(handle.tag)

    def submit_handles(self):
        for tag, handle in self.handles.items():
            self.submit_handle(tag, handle)

    def submit_handle(self, tag, handle):
        p = self.executor.submit(self._wrap_handle, handle, self.queue)
        self.processes[tag] = p
        return p

    def run_forever(self, debug=True):
        self.submit_handles()
        while True:
            tag = self.queue.get()
            p = self.processes.get(tag)
            if not p.done():
                logging.debug(f"tag: {tag} error {p.exception()}")
            if debug:
                logging.info(f"tag: {p}")
            self.submit_handle(tag, self.handles.get(tag))

    def close(self):
        self.executor.shutdown()
        self.queue.close()

