import logging
import os
import sys
import threading

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.insert(0, BASE_DIR)

from core.config_manager import load_config, save_config
from core.area_screenshot import capture_area
from core.hotkey import HotkeyManager
from ui.settings_window import SettingsWindow
from ui.tray import TrayIcon

ICON_PATH = os.path.join(BASE_DIR, "assets", "icon.ico")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def set_auto_start(enable):
    import winreg
    app_name = "ScreenshotTool"
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
        if enable:
            if getattr(sys, 'frozen', False):
                exe_path = sys.executable
            else:
                exe_path = f'"{sys.executable}" "{os.path.abspath(__file__)}"'
            winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
            logger.info("已设置开机自启")
        else:
            try:
                winreg.DeleteValue(key, app_name)
            except FileNotFoundError:
                pass
            logger.info("已取消开机自启")
        winreg.CloseKey(key)
    except Exception as e:
        logger.error("设置开机自启失败: %s", e)


class App:

    def __init__(self):
        self.config = load_config()
        self.hotkey_manager = HotkeyManager()
        self.tray = None
        self._register_hotkey()

    def _register_hotkey(self):
        self.hotkey_manager.unregister_all()
        self.hotkey_manager.register(
            self.config["hotkey"],
            self._on_screenshot,
            name="screenshot"
        )

    def _on_screenshot(self):
        logger.info("触发框选截图")
        capture_area(self.config["save_path"])

    def _on_settings(self):
        logger.info("打开设置窗口")
        threading.Thread(
            target=self._show_settings,
            daemon=True
        ).start()

    def _show_settings(self):
        def on_save(new_config):
            self.config = new_config
            save_config(new_config)
            self._register_hotkey()
            set_auto_start(new_config.get("auto_start", False))
            if self.tray:
                self.tray.update_tooltip(f"截图工具 ({new_config['hotkey']})")

        window = SettingsWindow(self.config, on_save=on_save)
        window.show()

    def _on_exit(self):
        logger.info("退出截图工具")
        self.hotkey_manager.unregister_all()
        if self.tray:
            self.tray.stop()

    def run(self):
        set_auto_start(self.config.get("auto_start", False))

        self.tray = TrayIcon(
            ICON_PATH,
            on_screenshot=self._on_screenshot,
            on_settings=self._on_settings,
            on_exit=self._on_exit
        )

        logger.info("截图工具已启动 | 快捷键: %s | 保存: %s",
                     self.config["hotkey"], self.config["save_path"])

        tray_thread = threading.Thread(target=self.tray.run, daemon=True)
        tray_thread.start()

        self.hotkey_manager.wait()


if __name__ == "__main__":
    app = App()
    app.run()
