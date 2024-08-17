flag_not_support = False
try:
    from util.plugin_dev.api.v1.bot import Context, AstrMessageEvent, CommandResult
    from util.plugin_dev.api.v1.config import *
except ImportError:
    flag_not_support = True
    print("导入接口失败。请升级到 AstrBot 最新版本。")
import json
import requests
import time
from .config import Config
deamonid = Config.mcsm_deamonid
url = Config.mcsm_url
apikey = Config.mcsm_apikey
whlielist = Config.whlielist
class McsmClient:
    def __init__(self, api_key: str, url: str):
        self.api_key = api_key
        self.url = url
        self.headers = {
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json"
        }

    def start_instance(self, uuid, daemon_id):
        resp = requests.get(f"{self.url}/api/protected_instance/open?apikey={self.api_key}&uuid={uuid}&daemonId={daemon_id}")
        return resp.json()

    def get_instance(self,instance_name,deamonid):
        url = f"{self.url}/api/service/remote_service_instances?apikey={self.api_key}&instance_name={instance_name}&daemonId={deamonid}&page=1&page_size=10&status="
        resp = requests.get(url,headers=self.headers)
        return resp.json().get("data",{}).get("data",[])


class Main:
    def __init__(self, context: Context) -> None:
        self.context = context
        self.context.register_commands("astrbot_plugin_mcsm_instance_start", "start", "允许指定用户启动Mcsm中的实例。", 1, self.mcsm_start)

    def mcsm_start(self, message: AstrMessageEvent, context: Context):
        mcsm = McsmClient(api_key=apikey, url=url)
        if message.message_obj.sender.user_id in whlielist:
            n = message.message_str.split(" ")[1]
            instanceid = mcsm.get_instance(instance_name=n,deamonid=deamonid)[0].get("instanceUuid")
            mcsm.start_instance(uuid=instanceid,daemon_id=deamonid)
            return CommandResult().message(f"已开启实例：{n}\nuuid:{instanceid},time:{time.time()}").use_t2i(False)
        else:
            return CommandResult().message("你没有权限使用此命令").use_t2i(False)
