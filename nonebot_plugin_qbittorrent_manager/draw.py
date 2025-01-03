from PIL import Image
from .config import state_name
from .tools import circle_corner, draw_form


async def draw_torrent_list(torrent_data: dict) -> Image.Image:
    """
    绘制torrent列表
    :param torrent_data:
    :return:
    """
    draw_data = [[
        {"color": "#000000", "size": 26, "text": "id"},
        {"color": "#000000", "size": 26, "text": "标题"},
        {},
        {},
        {"color": "#000000", "size": 26, "text": "状态"},
        {"color": "#000000", "size": 26, "text": "文件大小/剩余大小"},
        {},
        {"color": "#000000", "size": 26, "text": "进度"},
        {"color": "#000000", "size": 26, "text": "标签"},
        {"color": "#000000", "size": 26, "text": "分类"},
    ]]
    for torrent_id in torrent_data:
        torrent = torrent_data[torrent_id]
        name = str(torrent.get("name"))
        if len(name) > 25:
            name = name[:23] + "..."
        draw_data.append([
            {"color": "#000000", "size": 22, "text": torrent_id},
            {"color": "#000000", "size": 22, "text": name},
            {},
            {},
            {"color": "#000000", "size": 22, "text": state_name[str(torrent.get("state"))]},
            {"color": "#000000", "size": 22,
             "text": f"{size_text(torrent.get('size'))}/{size_text(torrent.get('size') - torrent.get('completed'))}"},
            {},
            {"color": "#000000", "size": 22, "text": "{:.2f}%".format(torrent.get('download_state'))},
            {"color": "#000000", "size": 22, "text": torrent.get('tags')},
            {"color": "#000000", "size": 22, "text": torrent.get('category')},
        ])

    x = 1200
    y = 0
    y += 70 + 28

    form_image = await draw_form(draw_data, x - 90)

    y += form_image.size[1]

    image = Image.new("RGBA", (x, y), "#F2F2F2")

    paste_image = Image.new("RGBA", (x - 44, form_image.size[1]), "#000000")
    paste_image = circle_corner(paste_image, 20)
    image.alpha_composite(paste_image, (22, 25))
    paste_image = Image.new("RGBA", (x - 46, form_image.size[1] - 2), "#FFFFFF")
    paste_image = circle_corner(paste_image, 19)
    image.alpha_composite(paste_image, (23, 26))

    image.alpha_composite(form_image, (45, 30))

    return image


def size_text(num: int) -> str:
    """
    转换数据单位
    :param num:byte大小
    :return:数字+单位。例：123Mb
    """
    if num is None:
        return ""
    units = ["B", "Kb", "Mb", "Gb", "Tb", "Pb", "Eb"]
    for unit in units:
        if num < 1024:
            text = "{:.2f}".format(num)
            text = text.removesuffix("0").removesuffix(".0")
            return f"{text}{unit}"
        num /= 1024
    return f"{num}{units[-1]}"









