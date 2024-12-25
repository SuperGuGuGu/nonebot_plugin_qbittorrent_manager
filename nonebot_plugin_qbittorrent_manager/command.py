import json
import re
from nonebot import logger
from .config import menu_data, state_name
from .qb_api import call_api


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
    download_data = {"urls": []}
    args_list = args.split(" ")
    jump_num = 0
    for i, arg in enumerate(args_list):
        if jump_num > 0:
            jump_num -= 1
        elif arg in ["-tag", "-t"]:
            download_data["tag"] = args_list[i + 1]
            jump_num += 1
        elif arg in ["-savepath", "-path", "-p"]:
            download_data["savepath"] = args_list[i + 1]
            jump_num += 1
        elif arg in ["-category", "-c"]:
            download_data["category"] = args_list[i + 1]
            jump_num += 1
        else:
            # magnet_links = re.findall(r'[a-zA-Z0-9]{40}[a-zA-Z0-9&=.\[\]\-]*', arg)
            magnet_links = re.findall(r'[a-zA-Z0-9]{40}', arg)
            for link in magnet_links:
                if link not in download_data["links"]:
                    download_data["urls"].append(link)
                    logger.debug(f"解析到链接：{link}")

    # 提交任务
    task_data = {
        "num": 0,
        "succeed": 0,
        "error": 0,
    }
    for url in download_data["urls"]:
        task_data["num"] += 1
        post_data = {"urls": url}
        if download_data.get("category") is not None:
            post_data["category"] = download_data.get("category")
        if download_data.get("tag") is not None:
            post_data["tag"] = download_data.get("tag")
        if download_data.get("savepath") is not None:
            post_data["savepath"] = download_data.get("savepath")
        try:
            data = await call_api("/api/v2/torrents/add", post_data=post_data)
            if data.text == "Ok.":
                task_data["succeed"] += 1
            else:
                logger.error(data.text)
                task_data["error"] += 1
        except Exception as e:
            logger.debug("e")
            logger.debug(e)
            task_data["error"] += 1

    # 组装返回信息
    return_msg = f"提交{task_data['num']}个任务，成功{task_data['succeed']}个"

    return return_msg


async def command_download_list(args: str):
    # 解析列表参数
    list_data = {}
    args_list = args.split(" ")
    jump_num = 0
    for i, arg in enumerate(args_list):
        if jump_num > 0:
            jump_num -= 1
        elif arg in ["-tag", "-t"]:
            list_data["tag"] = args_list[i + 1]
            jump_num += 1
        elif arg in ["-savepath", "-path", "-p"]:
            return "查看列表不支持文件夹参数"
        elif arg in ["-category", "-c"]:
            list_data["category"] = args_list[i + 1]
            jump_num += 1

    # 获取列表
    try:
        data = await call_api("/api/v2/torrents/info", post_data=list_data)
        logger.success("获取列表成功")
    except Exception as e:
        logger.error(e)
        return "api返回错误"

    # 排序列表
    download_list = json.loads(data.text)
    download_data = {}
    category_list = []  # 分类列表
    for data in download_list:
        num = 5
        torrent_id = data["hash"]
        for i in range(len(data["hash"]) - num):
            if data["hash"][:num + i] not in download_data.keys():
                torrent_id = data["hash"][:num + i]
                break
        if data["completed"] != 0:
            data["download_state"] = data["completed"] / (data["completed"] + data["amount_left"]) * 100
        else:
            data["download_state"] = 0

        download_data[torrent_id] = data
        if data["category"] not in category_list:
            category_list.append(data["category"])
    download_data = dict(sorted(download_data.items(), key=lambda item: item[1]['download_state'], reverse=True))
    message = ""
    for category in category_list:
        if category == "":
            category = "未分类"
        message += f"{category}: \n"
        for torrent_id in download_data:
            if category == download_data[torrent_id]['category']:
                message += f"  {torrent_id}: "
                message += f"{int(download_data[torrent_id]['download_state'])}% "
                message += f"{state_name[download_data[torrent_id]['state']]}\n"

    if message == "":
        return "暂无任务"
    return message
