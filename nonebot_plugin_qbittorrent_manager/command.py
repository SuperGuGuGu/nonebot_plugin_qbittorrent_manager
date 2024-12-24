from .config import menu_data


async def command_help():
    return_msg = "指令列表："
    for command in menu_data:
        return_msg += f"\n{command['trigger_method']}: {command['func']}"
    return return_msg


async def command_download(args: str):
    if args in ["", " "]:
        return "请添加要下载的内容，例：" + '"qb下载 xxx"'
    return_msg = []
    # 解析链接

    # 提交任务

    # 返回消息

    return return_msg
