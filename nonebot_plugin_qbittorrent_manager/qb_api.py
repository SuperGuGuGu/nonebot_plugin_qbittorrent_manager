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



