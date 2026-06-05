import json
import logging
import os
import sys

logger = logging.getLogger(__name__)

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

DEFAULT_CONFIG = {
    "save_path": os.path.join(BASE_DIR, "Screenshots"),
    "hotkey": "ctrl+shift+s",
    "auto_start": False
}


def load_config():
    if not os.path.exists(CONFIG_FILE):
        logger.info("配置文件不存在，使用默认配置")
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        for key, value in DEFAULT_CONFIG.items():
            config.setdefault(key, value)
        return config
    except (json.JSONDecodeError, IOError) as e:
        logger.error("读取配置文件失败: %s，使用默认配置", e)
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()


def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        logger.info("配置已保存到 %s", CONFIG_FILE)
    except IOError as e:
        logger.error("保存配置文件失败: %s", e)
