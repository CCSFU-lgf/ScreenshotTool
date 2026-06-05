# 📸 ScreenshotTool - Windows 截图工具

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=flat-square&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=flat-square&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**一款轻量级、高效的 Windows 框选截图工具，支持全局热键和系统托盘**

[功能特点](#-功能特点) • [快速开始](#-快速开始) • [使用方法](#-使用方法) • [配置说明](#-配置说明) • [打包部署](#-打包部署)

</div>

---

## 📖 简介

ScreenshotTool 是一款使用 Python 开发的 Windows 桌面截图工具。它运行在后台，通过全局快捷键随时触发框选截图，截图自动保存并复制到剪贴板，非常适合日常办公和开发使用。

## ✨ 功能特点

| 功能 | 描述 |
|:-----|:-----|
| 🖱️ **框选截图** | 按下快捷键进入全屏覆盖模式，鼠标拖拽选择截图区域 |
| 📋 **自动复制** | 截图完成后自动复制到系统剪贴板，可直接粘贴使用 |
| 💾 **自动保存** | 截图以时间戳命名，自动保存到指定目录 |
| ⌨️ **全局热键** | 支持自定义全局快捷键，随时一键截图 |
| 🔔 **系统托盘** | 最小化到系统托盘，不占用任务栏空间 |
| 🚀 **开机自启** | 可选开机自动启动，无需手动运行 |
| ⚙️ **图形设置** | 提供可视化设置界面，轻松配置各项参数 |

## 🚀 快速开始

### 环境要求

- Windows 10/11
- Python 3.7+

### 安装步骤

1. **克隆项目**

```bash
git clone https://github.com/yourusername/ScreenshotTool.git
cd ScreenshotTool
```

2. **安装依赖**

```bash
pip install -r requirements.txt
```

3. **运行程序**

```bash
python main.py
```

### 依赖说明

| 包名 | 用途 |
|:-----|:-----|
| `mss` | 高性能屏幕截图 |
| `pillow` | 图像处理与保存 |
| `keyboard` | 全局快捷键监听 |
| `pystray` | 系统托盘图标 |
| `pywin32` | Windows 剪贴板操作 |

## 📌 使用方法

### 基本操作

1. 运行程序后，系统托盘会出现截图工具图标
2. 按下快捷键 `Ctrl + Shift + A`（默认）进入截图模式
3. **鼠标拖拽** 选择要截图的区域
4. 点击 **✓（绿色）** 确认截图，或点击 **✕（红色）** 取消
5. 截图将自动保存并复制到剪贴板

### 快捷操作

| 操作 | 说明 |
|:-----|:-----|
| `鼠标左键拖拽` | 选择截图区域 |
| `鼠标右键` | 清除当前选区 |
| `Esc` | 取消截图 |
| `✓` 按钮 | 确认并保存截图 |
| `✕` 按钮 | 取消本次截图 |

### 系统托盘菜单

右键点击托盘图标，可以：
- 📸 **截图** - 立即触发截图
- ⚙️ **设置** - 打开设置窗口
- ❌ **退出** - 退出程序

## ⚙️ 配置说明

配置文件 `config.json` 位于程序根目录：

```json
{
    "save_path": "Screenshots",
    "hotkey": "ctrl+shift+a",
    "auto_start": false
}
```

| 参数 | 类型 | 说明 |
|:-----|:-----|:-----|
| `save_path` | String | 截图保存目录，支持相对路径和绝对路径 |
| `hotkey` | String | 全局快捷键，支持 `ctrl`、`shift`、`alt` 组合 |
| `auto_start` | Boolean | 是否开机自动启动 |

## 📦 打包部署

使用 PyInstaller 打包为独立可执行文件：

```bash
# 方式一：运行打包脚本
build.bat

# 方式二：手动打包
pip install -r requirements.txt
pyinstaller -F -w --icon=assets/icon.ico --add-data "assets;assets" --name ScreenshotTool main.py
```

打包完成后，可执行文件位于 `dist/ScreenshotTool.exe`。

## 📁 项目结构

```
ScreenshotTool/
├── main.py                 # 程序入口
├── config.json             # 配置文件
├── requirements.txt        # Python 依赖
├── build.bat               # 打包脚本
├── create_icon.py          # 图标生成工具
├── assets/                 # 资源文件
│   └── icon.ico            # 应用图标
├── core/                   # 核心模块
│   ├── config_manager.py   # 配置管理
│   ├── hotkey.py           # 快捷键管理
│   ├── screenshot.py       # 全屏截图
│   └── area_screenshot.py  # 区域截图
├── ui/                     # 界面模块
│   ├── tray.py             # 系统托盘
│   └── settings_window.py  # 设置窗口
└── Screenshots/            # 截图保存目录
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源 - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

**如果觉得有用，请给个 ⭐ Star 支持一下！**

Made with ❤️ by [Your Name]

</div>
