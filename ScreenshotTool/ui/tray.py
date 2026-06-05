import logging
import os

import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem

logger = logging.getLogger(__name__)


def _create_default_icon():
    img = Image.new("RGB", (64, 64), color="#2196F3")
    draw = ImageDraw.Draw(img)
    draw.rectangle([12, 12, 52, 52], outline="white", width=3)
    draw.rectangle([24, 24, 40, 40], fill="white")
    return img


def _load_icon(icon_path):
    if icon_path and os.path.exists(icon_path):
        return Image.open(icon_path)
    logger.warning("图标文件不存在: %s，使用默认图标", icon_path)
    return _create_default_icon()


class TrayIcon:

    def __init__(self, icon_path, on_screenshot, on_settings, on_exit):
        image = _load_icon(icon_path)

        menu = (
            MenuItem("截图", on_screenshot),
            pystray.Menu.SEPARATOR,
            MenuItem("设置", on_settings),
            pystray.Menu.SEPARATOR,
            MenuItem("退出", on_exit),
        )

        self.icon = pystray.Icon(
            "ScreenshotTool",
            image,
            "截图工具",
            menu
        )

    def update_tooltip(self, text):
        self.icon.title = text

    def run(self):
        self.icon.run()

    def stop(self):
        self.icon.stop()
