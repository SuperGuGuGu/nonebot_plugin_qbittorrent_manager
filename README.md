<div align="center">
  <p><img src="/image/README/title.png" width="480" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-qbittorrent-manager

_✨ qbittorrent管理器 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/SuperGuGuGu/nonebot_plugin_qbittorrent_manager.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-qbittorrent-manager">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-qbittorrent-manager.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>

## 📖 介绍

qbittorrent管理器，可以远程管理qb下载内容

跨平台

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-qbittorrent-manager

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-qbittorrent-manager

</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-qbittorrent-manager

</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-qbittorrent-manager

</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-qbittorrent-manager

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_qbittorrent_manager"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

|       配置项       | 必填 |           默认值            |          说明          |            示例            |
|:---------------:|:--:|:------------------------:|:--------------------:|:------------------------:|
|     qbm_url     | 是  |            无             |        qb的url        | "http://127.0.0.1:8080"  |
|  qbm_username   | 是  |            无             |         用户名称         |        "username"        |
|  qbm_password   | 是  |            无             |         用户密码         |        "password"        |
| qbm_enable_user | 否  |            []            | 有使用权限的用户，默认响应所有用户的操作 |        ["12345"]         |
|  qbm_send_text  | 否  |          false           |      禁用绘图，只发送文本      |           true           |
|  qbm_basepath   | 否  | "./qbittorrent_manager/" |      插件数据存放文件夹       | "./qbittorrent_manager/" |

## 🎉 使用

### 指令表

- ✅: 支持
- 🚧: 部分支持或正在完善
- 🗓️️: 计划中

|  指令  |     说明      | 需要at | 功能实现 | 图形界面 |
|:----:|:-----------:|:----:|:----:|:----:|
| qb帮助 |    指令列表     |  是   |  ✅   | 🗓️  |
| qb下载 |    下载文件     |  是   |  ✅️  | 🗓️  |
| qb列表 |   目前的任务列表   |  是   |  ✅️  | 🗓️  |
| qb删除 |   删除指定任务    |  是   |  ✅️  | 🗓️  |
| qb修改 | 修改分类、标签、文件夹 |  是   | 🗓️  | 🗓️  |

### 说明

qb下载、qb列表、qb删除 可带参数执行

可选参数:

    tag, t: 标签
    path, path, p: 下载的路径
    category, c: 分类
    state:

###

    /qb下载 -tag 视频 xxx  # 将url的内容下载并添加tag[视频]

### 效果图

[图片.jpg]
