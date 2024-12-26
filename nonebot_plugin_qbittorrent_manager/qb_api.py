import json

import httpx
from httpx import codes as status_code
from nonebot import logger
from .config import qbm_username, qbm_password
from .tools import qbm_cache, basepath, qb_url


async def client(path, post_data=None, timeout=10):
    if post_data is None:
        async with httpx.AsyncClient() as http_client:
            data = await http_client.get(
                f"{qb_url}{path}",
                timeout=timeout,
                cookies=qbm_cache.get("cookies")
            )
    else:
        async with httpx.AsyncClient() as http_client:
            data = await http_client.post(
                f"{qb_url}{path}",
                data=post_data,
                timeout=timeout,
                cookies=qbm_cache.get("cookies")
            )
    if data.status_code == status_code.OK:
        return data
    logger.error(f"url: {qb_url}{path}")
    logger.error(f"data: {data.text}")
    raise "api返回错误"


async def login():
    post_data = {
        "username": qbm_username,
        "password": qbm_password
    }
    data = await client("/api/v2/auth/login", post_data=post_data)
    if data.text != "Ok.":
        logger.error("登陆失败")
        raise "登陆失败"

    headers: list[str] = data.headers.get("set-cookie").split("; ")
    for header in headers:
        if header.startswith("SID"):
            qbm_cache["cookies"] = {"SID": header.split("=")[1]}

    if qbm_cache.get("cookies") is None:
        logger.error("登陆失败")
        raise "登陆失败"

    logger.success("登陆成功")
    return "succeed"


async def call_api(path: str, params: dict = None, post_data: dict = None):
    """
    请求qb的api
    :param path:
    :param params:
    :param post_data:
    :return:
    """
    logger.debug(f"call_api: {path}")
    if params is None:
        params = {}
    if qbm_cache.get("cookies") is None:
        try:
            await login()
        except Exception as e:
            return "登陆失败"

    if len(list(params)) != 0:
        path += "?"
        for p in params:
            path += f"{p}={params[p]}&"
        path = path.removesuffix("&")

    return await client(path, post_data=post_data)


async def get_torrent_list(select_data: dict = None) -> dict | str:
    """
    获取torrent列表
    :param select_data:分类列表
    :return:
    """
    if select_data is None:
        select_data = {}
    # 获取列表
    try:
        data = await call_api("/api/v2/torrents/info")
        logger.success("获取列表成功")
    except Exception as e:
        logger.error("call_api失败: /api/v2/torrents/info")
        raise "call_api失败"

    # 整理列表
    download_list = json.loads(data.text)
    download_data = {}
    for data in download_list:
        num = 5
        torrent_id = data["hash"]
        for i in range(len(data["hash"]) - num):
            if data["hash"][:num + i] not in download_data.keys():
                torrent_id = data["hash"][:num + i]
                break
        # 添加下载进度
        if data["completed"] != 0:
            data["download_state"] = data["completed"] / (data["completed"] + data["amount_left"]) * 100
        else:
            data["download_state"] = 0
        download_data[torrent_id] = data

    # 排序
    new_download_data = {}
    category_list = []
    for torrent in download_data:
        if select_data.get("tag") is not None:
            if select_data.get("tag") not in download_data[torrent]["tags"].split(", "):
                continue
        if select_data.get("category") is not None:
            if select_data.get("category") not in download_data[torrent]["category"].split(", "):
                continue
        if download_data[torrent]["category"] not in category_list:
            category_list.append(download_data[torrent]["category"])
        new_download_data[torrent] = download_data[torrent]

    download_data = dict(sorted(new_download_data.items(), key=lambda item: item[1]['download_state'], reverse=True))

    return download_data

