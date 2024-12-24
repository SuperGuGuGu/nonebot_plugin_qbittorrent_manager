<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
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

|      配置项       | 必填 | 默认值 |        说明        |           示例            |
|:--------------:|:--:|:---:|:----------------:|:-----------------------:|
|      url       | 是  |  无  |      qb的url      | "http://127.0.0.1:8080" |
|  enable_group  | 否  | []  | 启用的群聊,为空时所有群均响应  |        ["12345"]        |
| enable_private | 否  | []  | 启用的私聊,为空时所有私聊均响应 |        ["12345"]        |

## 🎉 使用

### 指令表
- ✅: 支持
- 🚧: 部分支持或正在完善
- 🗓️️: 计划中

|  指令  |   说明    | 功能实现 |
|:----:|:-------:|:----:|
|  帮助  |  指令列表   | 🗓️ |
|  下载  |  下载文件   |  🗓️   |
| 下载列表 | 目前的任务列表 |  🗓️   |

### 说明

下载、下载列表可带参数执行

可选参数: tag, t, folder, f, state

    下载 -tag 视频 url  # 将url的内容下载并添加tag[视频]

### 效果图

[图片.jpg]
