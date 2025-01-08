import re
from nonebot import logger
from .config import menu_data, state_name, send_text
from .draw import draw_torrent_list
from .qb_api import call_api, get_torrent_list


async def command_help():
    return_msg = "指令列表："
    for command in menu_data:
        if command['trigger_method'] == "qb帮助":
            continue
        return_msg += f"\n{command['trigger_method']}: {command['func']}"
    return return_msg


async def command_download(args: str):
    if args in ["", " "]:
        return "请添加要下载的内容，例：" + '"qb下载 xxx"'

    # 解析链接
    download_data = {"urls": {}}
    args_list = args.split(" ")
    jump_num = 0
    for i, arg in enumerate(args_list):
        if jump_num > 0:
            jump_num -= 1
        elif arg in ["-tag", "-t"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            download_data["tag"] = args_list[i + 1]
            jump_num += 1
        elif arg in ["-savepath", "-path", "-p"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            download_data["savepath"] = args_list[i + 1]
            jump_num += 1
        elif arg in ["-category", "-c"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            download_data["category"] = args_list[i + 1]
            jump_num += 1
        else:
            magnet_links: list[str] = re.findall(r'[a-zA-Z0-9]{30,60}[a-zA-Z0-9&=.\[\]\-]*', arg)
            # magnet_links = re.findall(r'[a-zA-Z0-9]{40}', arg)
            for link in magnet_links:
                if "&" in link:
                    l = link.split("&", 1)[0]
                    args = link.split("&", 1)[1]
                    link = l
                else:
                    args = ""

                if link not in download_data["urls"].keys():
                    download_data["urls"][link] = args
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
        if download_data["urls"][url] != "":
            # 解析链接参数
            # logger.debug(f"解析链接参数: {download_data['urls'][url]}")
            # download_data['urls'][url] = "dn=xxx.mp4"
            pass
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
    return f"提交{task_data['num']}个任务，成功{task_data['succeed']}个"


async def command_download_list(args: str):
    # 解析列表参数
    select_data = {}
    args_list = args.split(" ")
    jump_num = 0
    for i, arg in enumerate(args_list):
        if jump_num > 0:
            jump_num -= 1
        elif arg in ["-tag", "-t"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            select_data["tag"] = args_list[i + 1]
            jump_num += 1
        elif arg in ["-savepath", "-path", "-p"]:
            return "查看列表不支持文件夹参数"
        elif arg in ["-category", "-c"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            select_data["category"] = args_list[i + 1]
            jump_num += 1

    # 获取列表
    try:
        download_data: dict[str, dict] = await get_torrent_list(select_data=select_data)
    except Exception as e:
        return "api连接失败"

    category_list = []
    for torrent in download_data:
        if download_data[torrent]["category"] not in category_list:
            category_list.append(download_data[torrent]["category"])

    # 组装返回信息
    if send_text is True:
        message = ""
        for category in category_list:
            if category == "":
                message += f"未分类: \n"
            else:
                message += f"{category}: \n"
            for torrent_id in download_data:
                if category == download_data[torrent_id]['category']:
                    message += f"  {torrent_id}: "
                    message += f"{int(download_data[torrent_id]['download_state'])}% "
                    message += f"{state_name[download_data[torrent_id]['state']]}\n"

        if message == "":
            return "暂无任务"
        return message

    return await draw_torrent_list(download_data)


async def command_delete(args: str):
    if args in ["", " "]:
        return '请添加要删除的torrent，例: "/qb删除 xxxx"'

    # 解析列表参数
    select_data = {}
    args_list = args.split(" ")
    jump_num = 0
    for i, arg in enumerate(args_list):
        if jump_num > 0:
            jump_num -= 1
        elif arg in ["-tag", "-t"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            select_data["tag"] = args_list[i + 1]
            jump_num += 1
        elif arg in ["-savepath", "-path", "-p"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            select_data["savepath"] = args_list[i + 1]
            jump_num += 1
        elif arg in ["-category", "-c"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            select_data["category"] = args_list[i + 1]
            jump_num += 1
        elif arg not in [""]:
            select_data["url"] = arg

    # 获取列表
    try:
        download_data: dict[str, dict] = await get_torrent_list(select_data=select_data)
    except Exception as e:
        return "api连接失败"

    delete_list = {}
    for torrent in download_data:
        select = True
        if select_data.get("url") is not None:
            if select_data.get("url") != download_data[torrent]["hash"] and select_data.get("url") != torrent:
                select = False
        if select_data.get("category") is not None:
            if select_data.get("category") != download_data[torrent]["category"]:
                select = False
        if select_data.get("savepath") is not None:
            if (str(select_data.get("savepath")).replace("/", "\\") ==
                    download_data[torrent]["download_path"].replace("/", "\\")):
                select = False
        if select_data.get("tag") is not None:
            if select_data.get("tag") not in download_data[torrent]["tags"].split(", "):
                select = False
        if select is True:
            # delete_list.append(download_data[torrent]["hash"])
            delete_list[torrent] = download_data[torrent]

    # 提交任务
    task_data = {
        "num": 0,
        "succeed": 0,
        "error": 0,
    }

    if len(delete_list) == 0:
        return "找不到要删除的torrent"

    for torrent in delete_list:
        task_data["num"] += 1
        post_data = {
            "hashes": delete_list[torrent]['hash'],
            "deleteFiles": False
        }
        try:
            task_data["succeed"] += 1
            await call_api(f"/api/v2/torrents/delete", post_data=post_data)
        except Exception as e:
            logger.error("e")
            logger.error(e)
            task_data["error"] += 1

    # 组装返回信息
    return f"提交删除{task_data['num']}个任务，成功{task_data['succeed']}个"


async def command_deep_delete(args: str):
    if args in ["", " "]:
        return '请添加要删除的torrent，例: "/qb完全删除 xxxx"'

    # 解析列表参数
    select_data = {}
    args_list = args.split(" ")
    jump_num = 0
    for i, arg in enumerate(args_list):
        if jump_num > 0:
            jump_num -= 1
        elif arg in ["-tag", "-t"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            select_data["tag"] = args_list[i + 1]
            jump_num += 1
        elif arg in ["-savepath", "-path", "-p"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            select_data["savepath"] = args_list[i + 1]
            jump_num += 1
        elif arg in ["-category", "-c"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            select_data["category"] = args_list[i + 1]
            jump_num += 1
        elif arg not in [""]:
            select_data["url"] = arg

    # 获取列表
    try:
        download_data: dict[str, dict] = await get_torrent_list(select_data=select_data)
    except Exception as e:
        return "api连接失败"

    delete_list = {}
    for torrent in download_data:
        select = True
        if select_data.get("url") is not None:
            if select_data.get("url") != download_data[torrent]["hash"] and select_data.get("url") != torrent:
                select = False
        if select_data.get("category") is not None:
            if select_data.get("category") != download_data[torrent]["category"]:
                select = False
        if select_data.get("savepath") is not None:
            if (str(select_data.get("savepath")).replace("/", "\\") ==
                    download_data[torrent]["download_path"].replace("/", "\\")):
                select = False
        if select_data.get("tag") is not None:
            if select_data.get("tag") not in download_data[torrent]["tags"].split(", "):
                select = False
        if select is True:
            # delete_list.append(download_data[torrent]["hash"])
            delete_list[torrent] = download_data[torrent]

    # 提交任务
    task_data = {
        "num": 0,
        "succeed": 0,
        "error": 0,
    }

    if len(delete_list) == 0:
        return "找不到要删除的torrent"

    for torrent in delete_list:
        task_data["num"] += 1
        post_data = {
            "hashes": delete_list[torrent]['hash'],
            "deleteFiles": True
        }
        try:
            task_data["succeed"] += 1
            await call_api(f"/api/v2/torrents/delete", post_data=post_data)
        except Exception as e:
            logger.error("e")
            logger.error(e)
            task_data["error"] += 1

    # 组装返回信息
    return f"提交删除{task_data['num']}个任务，成功{task_data['succeed']}个"


async def command_edit(args: str):
    if args in ["", " "]:
        return "请添加要下载的内容，例：" + '"qb下载 xxx"'

    try:
        torrent_data: dict = await get_torrent_list()
    except Exception as e:
        logger.error(e)
        return "api连接失败"

    # 解析链接
    edit_data = {"urls": {}}
    args_list = args.split(" ")
    jump_num = 0
    for i, arg in enumerate(args_list):
        if jump_num > 0:
            jump_num -= 1
        elif arg in ["-tag", "-t"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            edit_data["tag"] = args_list[i + 1]
            jump_num += 1
        elif arg in ["-savepath", "-path", "-p"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            edit_data["savepath"] = args_list[i + 1]
            jump_num += 1
        elif arg in ["-category", "-c"]:
            if i + 1 > len(args_list) - 1:
                return "参数类型后需要添加参数"
            edit_data["category"] = args_list[i + 1]
            jump_num += 1
        else:
            if arg in torrent_data.keys():
                edit_data["urls"][torrent_data[arg]["hash"]] = ""
            else:
                edit_data["urls"][arg] = ""

    # 提交任务
    error_msg = {}
    for url in edit_data["urls"]:
        if edit_data.get("tag") is not None:
            try:
                await call_api(
                    "/api/v2/torrents/addTags",
                    post_data={
                        "hashes": url,
                        "tags": edit_data.get("tag")})
                error = None
            except Exception as e:
                error = "api连接出错"

            if error is not None:
                if url not in error_msg.keys():
                    error_msg[url] = [error]
                else:
                    error_msg[url].append(error)

        if edit_data.get("savepath") is not None:
            post_data = {"hashes": url, "location": edit_data.get("savepath")}
            data = await call_api("/api/v2/torrents/setLocation", post_data=post_data, not_raise=True)
            if data.status_code == 200:
                error = None
            elif data.status_code == 400:
                error = "保存路径为空"
            elif data.status_code == 403:
                error = "用户没有对目录的写入权限"
            elif data.status_code == 409:
                error = "无法创建保存路径目录"
            else:
                logger.warning("意外情况")
                logger.warning(data)
                logger.warning(data.text)
                error = "意外情况"
            if error is not None:
                if url not in error_msg.keys():
                    error_msg[url] = [error]
                else:
                    error_msg[url].append(error)

        if edit_data.get("category") is not None:
            post_data = {"hashes": url, "category": edit_data.get("category")}
            data = await call_api("/api/v2/torrents/setCategory", post_data=post_data)
            if data.text == "Ok.":
                continue
            logger.error(data.text)
            if url not in error_msg.keys():
                error_msg[url] = ["设置分类失败"]
            else:
                error_msg[url].append("设置分类失败")

    # 组装返回信息
    if error_msg == {}:
        return "修改成功"

    message = "以下内容出错："
    for torrent in error_msg:
        message += f"\n{torrent[:6]}:"
        for error in error_msg[torrent]:
            message += f"\n{error}:"

    return message
