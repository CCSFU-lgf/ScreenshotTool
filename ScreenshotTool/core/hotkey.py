import logging

import keyboard

logger = logging.getLogger(__name__)


class HotkeyManager:

    def __init__(self):
        self._hotkeys = {}

    def register(self, hotkey, callback, name="default"):
        self.unregister(name)
        try:
            keyboard.add_hotkey(hotkey, callback)
            self._hotkeys[name] = hotkey
            logger.info("快捷键已注册: %s -> %s", name, hotkey)
        except Exception as e:
            logger.error("注册快捷键失败 [%s]: %s", hotkey, e)

    def unregister(self, name="default"):
        if name in self._hotkeys:
            try:
                keyboard.remove_hotkey(self._hotkeys.pop(name))
            except Exception as e:
                logger.warning("移除快捷键失败 [%s]: %s", name, e)

    def unregister_all(self):
        for name in list(self._hotkeys):
            self.unregister(name)

    def wait(self):
        keyboard.wait()
