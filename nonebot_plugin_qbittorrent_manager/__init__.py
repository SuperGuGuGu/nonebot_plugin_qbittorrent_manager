from nonebot import logger
logger.info("ping")  # test3
from nonebot.plugin import PluginMetadata

_plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_qbittorrent_manager",
    description="qb管理器",
    usage="/help",
    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。
    homepage="https://github.com/SuperGuGuGu/nonebot_plugin_qbittorrent_manager",
    # 发布必填。
    # config=Config,
    # 插件配置项类，如无需配置可不填写。
    # supported_adapters={"~onebot.v11", "~telegram"},
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
)
