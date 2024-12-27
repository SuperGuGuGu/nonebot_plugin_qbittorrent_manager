import html
from PIL import Image
from nonebot import logger, require, on_command
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from nonebot.rule import to_me
from nonebot.adapters import Event

from .tools import save_image
from .config import Config, menu_data, enable_user
from .command import command_help, command_download, command_download_list, command_delete

require("nonebot_plugin_saa")
from nonebot_plugin_saa import Image as saaImage, MessageFactory
from nonebot_plugin_saa import Text as saaText

__plugin_meta__ = PluginMetadata(
    name="nonebot_plugin_qbittorrent_manager",
    description="qb管理器",
    usage="/qb帮助",
    type="application",
    # 发布必填，当前有效类型有：`library`（为其他插件编写提供功能），`application`（向机器人用户提供功能）。
    homepage="https://github.com/SuperGuGuGu/nonebot_plugin_qbittorrent_manager",
    # 发布必填。
    config=Config,
    # 插件配置项类，如无需配置可不填写。
    supported_adapters=inherit_supported_adapters(
        "nonebot_plugin_saa",
    ),
    # 支持的适配器集合，其中 `~` 在此处代表前缀 `nonebot.adapters.`，其余适配器亦按此格式填写。
    # 若插件可以保证兼容所有适配器（即仅使用基本适配器功能）可不填写，否则应该列出插件支持的适配器。
    extra={'menu_data': menu_data},
)

help_cmd = on_command("qb帮助", rule=to_me(), priority=10, block=False)


@help_cmd.handle()
async def help_msg(event: Event):
    if not event.get_type().startswith("message"):
        await help_cmd.finish()
    # msg: str = str(event.get_message().copy())
    # if msg == "":
    #     await help_cmd.finish()

    if event.get_user_id() not in enable_user and enable_user != []:
        await help_cmd.finish()

    msg = await command_help()

    await send(msg)
    await help_cmd.finish()


download_cmd = on_command("qb下载", rule=to_me(), priority=10, block=False)


@download_cmd.handle()
async def download_msg(event: Event):
    if not event.get_type().startswith("message"):
        await download_cmd.finish()
    msg: str = str(event.get_message().copy())
    if msg == "":
        await download_cmd.finish()

    if event.get_user_id() not in enable_user and enable_user != []:
        await help_cmd.finish()

    command_prefix = f"{msg.split('qb下载')[0]}qb下载"
    args = msg.removeprefix(command_prefix).removeprefix(" ")
    args = html.unescape(args)  # 反转义文字

    msg = await command_download(args=args)

    await send(msg)
    await download_cmd.finish()


download_list_cmd = on_command("qb列表", rule=to_me(), priority=10, block=False)


@download_list_cmd.handle()
async def download_msg(event: Event):
    if not event.get_type().startswith("message"):
        await download_list_cmd.finish()
    msg: str = str(event.get_message().copy())
    if msg == "":
        await download_list_cmd.finish()

    if event.get_user_id() not in enable_user and enable_user != []:
        await help_cmd.finish()

    command_prefix = f"{msg.split('qb列表')[0]}qb列表"
    args = msg.removeprefix(command_prefix).removeprefix(" ")
    args = html.unescape(args)  # 反转义文字

    msg = await command_download_list(args=args)

    await send(msg)
    await download_list_cmd.finish()


delete_cmd = on_command("qb删除", rule=to_me(), priority=10, block=False)


@delete_cmd.handle()
async def download_msg(event: Event):
    if not event.get_type().startswith("message"):
        await delete_cmd.finish()
    msg: str = str(event.get_message().copy())
    if msg == "":
        await delete_cmd.finish()

    if event.get_user_id() not in enable_user and enable_user != []:
        await help_cmd.finish()

    command_prefix = f"{msg.split('qb删除')[0]}qb删除"
    args = msg.removeprefix(command_prefix).removeprefix(" ")
    args = html.unescape(args)  # 反转义文字

    msg = await command_delete(args=args)

    await send(msg)
    await delete_cmd.finish()


async def send(msg):
    if type(msg) is not list:
        msg = [msg]

    saa_msg = []
    for m in msg:
        if type(m) is Image.Image:
            saa_msg.append(saaImage(await save_image(msg)))
        elif type(m) is bytes:
            saa_msg.append(saaImage(m))
        else:
            saa_msg.append(saaText(m))

    if not saa_msg:
        return

    msg_builder = MessageFactory(saa_msg)
    await msg_builder.send()
