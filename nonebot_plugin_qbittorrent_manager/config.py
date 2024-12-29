from nonebot import get_plugin_config, logger
from pydantic import BaseModel


class Config(BaseModel):
    qbm_url: str
    qbm_username: str
    qbm_password: str
    qbm_enable_user: list[str] = []
    qbm_send_text: bool = False
    qbm_basepath: str = "./qbittorrent_manager/"


menu_data = [
    {
        "trigger_method": "qb帮助",
        "func": "列出命令列表",
        "trigger_condition": " ",
        "brief_des": "qb帮助",
    },
    {
        "trigger_method": "qb下载",
        "func": "下载文件",
        "trigger_condition": " ",
        "brief_des": "qb下载 xxx",
    },
    {
        "trigger_method": "qb列表",
        "func": "列出qb任务列表",
        "trigger_condition": " ",
        "brief_des": "qb列表",
    },
    {
        "trigger_method": "qb删除",
        "func": "删除指定任务",
        "trigger_condition": " ",
        "brief_des": "qb删除 xxx",
    }
]

state_name = {
    "error": "错误/暂停",  # 发生一些错误，适用于暂停的种子
    "missingFiles": "文件丢失",  # Torrent 数据文件丢失
    "uploading": "正在做种/上传",  # 正在播种 Torrent 并传输数据
    "pausedUP": "已完成",  # Torrent 已暂停并已完成下载
    "queuedUP": "排队上传中",  # 已启用排队，并且 torrent 已排队等待上传
    "stalledUP": "正在做种",  # 正在种子 Torrent 中，但未建立任何连接
    "checkingUP": "已完成，正在检查",  # Torrent 已完成下载并正在检查
    "forcedUP": "强制上传中",  # Torrent 被迫上传并忽略队列限制
    "allocating": "正在分配磁盘空间",  # Torrent 正在分配磁盘空间以供下载
    "downloading": "正在下载",  # 正在下载 Torrent 并正在传输数据
    "metaDL": "准备下载",  # Torrent 刚刚开始下载并正在获取元数据
    "pausedDL": "已暂停且未完成",  # Torrent 已暂停且尚未完成下载
    "queuedDL": "排队下载中",  # 已启用排队，并且 torrent 已排队等待下载
    "stalledDL": "正在下载（等待连接）",  # 正在下载 Torrent，但未建立任何连接
    "checkingDL": "未完成，正在检查",  # 与 checkingUP 相同，但 torrent 尚未完成下载
    "forcedDL": "强制下载中",  # Torrent 被强制下载以忽略队列限制
    "checkingResumeData": "检查恢复数据",  # 在 qBt 启动时检查恢复数据
    "moving": "正在移动",  # Torrent 正在移动到另一个位置
    "unknown": "未知状态",  # 未知状态
}

plugin_config = get_plugin_config(Config)
qb_url = plugin_config.qbm_url
if not qb_url.startswith("http://") and not qb_url.startswith("https://"):
    logger.error("qbm_url配置出错，可能会导致无法正确连接，示例: 'http://127.0.0.1:8080'")
qbm_username = plugin_config.qbm_username
qbm_password = plugin_config.qbm_password
enable_user = plugin_config.qbm_enable_user
if len(enable_user) == 0:
    logger.warning("未配置enable_user，将响应所有用户的指令")
send_text = plugin_config.qbm_send_text
basepath = plugin_config.qbm_basepath
