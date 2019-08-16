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

用来自定义报警

# monitor 用来注册handle
