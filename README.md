# pymonitor
监控agent

# handle module 

用来收集监控指标
```python

class DiskMonitHandle(BaseHandle):
    # 收集了磁盘信息
    def get_metric(self):
        return psutil.disk_usage("/").percent

```
# alert module

用来自定义报警
``` python
class LackAlert(BaseAlert):
    # 飞书报警
    LackWebHook = "https://open.feishu.cn/open-apis/bot/hook/"
    _hook_id = None

    @classmethod
    def set_hook_id(cls, hook_id):
        cls._hook_id = hook_id

    def do_alert(self):
        requests.post(f'{self.LackWebHook}{self._hook_id}', json={"text": self.message()})

```


# monitor 用来注册handle
``` python

    monitor = Monitor()
    monitor.add_handle(CPUMonitHandle("cpu", 15, 10, AlertHandleClass=LackAlert, debug=True))
    monitor.add_handle(DiskMonitHandle("disk", 20, 25, AlertHandleClass=LackAlert, debug=True))
    try:
        monitor.run_forever()
    except Exception as e:
        monitor.close()

```
