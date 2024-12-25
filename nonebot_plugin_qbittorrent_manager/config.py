from nonebot import get_plugin_config
from pydantic import BaseModel, field_validator


# 我也不知道这个注释有什么用，pyc加的，删了它会骂我
# noinspection PyNestedDecorators
class Config(BaseModel):
    qbm_url: str
    qbm_username: str
    qbm_password: str
    qbm_enable_group: list[str] = []
    qbm_enable_private: list[str] = []
    qbm_send_text: bool = False
    qbm_basepath: str = "./qbittorrent_manager/"

    @field_validator("qbm_url")
    @classmethod
    def check_priority(cls, url: str) -> str:
        if url.startswith("http://") or url.startswith("https://"):
            return url
        raise ValueError("qbm_url需要配置一个url，例: 'http://127.0.0.1:8080'")


menu_data = [
    {
        "trigger_method": "qb帮助",
        "func": "列出命令列表",
        "trigger_condition": ' ',
        "brief_des": "qb帮助",
    },
    {
        "trigger_method": "qb下载",
        "func": "下载文件",
        "trigger_condition": ' ',
        "brief_des": "qb下载 xxx",
    },
    {
        "trigger_method": "qb列表",
        "func": "列出qb任务列表",
        "trigger_condition": ' ',
        "brief_des": "qb列表",
    }
]
plugin_config = get_plugin_config(Config)
qb_url = plugin_config.qbm_url
qbm_username = plugin_config.qbm_username
qbm_password = plugin_config.qbm_password
enable_group = plugin_config.qbm_enable_group
enable_private = plugin_config.qbm_enable_private
send_text = plugin_config.qbm_send_text
basepath = plugin_config.qbm_basepath
