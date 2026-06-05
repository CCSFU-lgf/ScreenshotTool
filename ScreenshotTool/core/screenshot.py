import io
import logging
import os
from datetime import datetime

import mss
import win32clipboard
from PIL import Image

logger = logging.getLogger(__name__)


def copy_to_clipboard(img):
    output = io.BytesIO()
    img.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]

    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    finally:
        win32clipboard.CloseClipboard()
    logger.info("已复制到剪贴板")


def capture(save_dir):
    os.makedirs(save_dir, exist_ok=True)

    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.png")
    filepath = os.path.join(save_dir, filename)

    try:
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            sct_img = sct.grab(monitor)
            img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            img.save(filepath)

        copy_to_clipboard(img)
        logger.info("全屏截图已保存: %s", filepath)
        return filepath
    except Exception as e:
        logger.error("全屏截图失败: %s", e)
        return None
