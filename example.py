from .handle import CPUMonitHandle, DiskMonitHandle
from .alert import LackAlert
from .monitor import Monitor

if __name__ == "__main__":
    LackAlert.set_hook_id("e067ec6bd0414db7b4fc62fbcf585e87")
    monitor = Monitor()
    monitor.add_handle(CPUMonitHandle("cpu", 15, 10, AlertHandleClass=LackAlert, debug=True))
    monitor.add_handle(DiskMonitHandle("disk", 20, 25, AlertHandleClass=LackAlert, debug=True))
    try:
        monitor.run_forever()
    except Exception as e:
        monitor.close()

