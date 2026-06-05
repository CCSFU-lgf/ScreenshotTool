import logging
import os
import tkinter as tk
from datetime import datetime

import mss
from PIL import Image

from core.screenshot import copy_to_clipboard

logger = logging.getLogger(__name__)


def _show_toast(text, duration=1500):
    win = tk.Tk()
    win.overrideredirect(True)
    win.attributes("-topmost", True)
    win.configure(bg="#1E88E5")

    screen_w = win.winfo_screenwidth()
    screen_h = win.winfo_screenheight()
    w, h = 220, 60
    x = (screen_w - w) // 2
    y = (screen_h - h) // 2
    win.geometry(f"{w}x{h}+{x}+{y}")

    label = tk.Label(
        win, text=text, font=("微软雅黑", 16, "bold"),
        fg="white", bg="#1E88E5"
    )
    label.pack(expand=True, fill=tk.BOTH)

    win.after(duration, win.destroy)
    win.mainloop()


class AreaSelector:

    def __init__(self, save_dir):
        self.save_dir = save_dir
        self.root = None
        self.canvas = None
        self.start_x = 0
        self.start_y = 0
        self.rect_id = None
        self.screenshot = None
        self.result = None
        self._btn_frame = None

    def run(self):
        self._capture_screen()
        self._create_overlay()
        self.root.mainloop()
        return self.result

    def _capture_screen(self):
        with mss.mss() as sct:
            monitor = sct.monitors[0]
            sct_img = sct.grab(monitor)
            self.screenshot = Image.frombytes(
                "RGB", sct_img.size, sct_img.bgra, "raw", "BGRX"
            )

    def _create_overlay(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.15)
        self.root.configure(bg="black")

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        self.canvas = tk.Canvas(
            self.root,
            width=screen_w,
            height=screen_h,
            highlightthickness=0,
            bg="black",
            cursor="cross"
        )
        self.canvas.pack()

        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.canvas.bind("<ButtonPress-3>", self._on_right_click)
        self.root.bind("<Escape>", lambda e: self._cancel())

    def _on_press(self, event):
        self._hide_confirm_buttons()
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id:
            self.canvas.delete(self.rect_id)
        self.rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y,
            self.start_x, self.start_y,
            outline="#0D47A1", width=3, fill="#0D47A1", stipple="gray50"
        )

    def _on_drag(self, event):
        self.canvas.coords(
            self.rect_id,
            self.start_x, self.start_y,
            event.x, event.y
        )

    def _on_release(self, event):
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)

        if abs(x2 - x1) < 5 or abs(y2 - y1) < 5:
            self._cancel()
            return

        self._region = (x1, y1, x2, y2)
        self._show_confirm_buttons(x2, y2)

    def _show_confirm_buttons(self, x, y):
        self._hide_confirm_buttons()

        self._btn_frame = tk.Frame(self.canvas, bg="#0D47A1", bd=2, relief="solid",
                                    highlightbackground="#0D47A1", highlightthickness=2)
        self.canvas.create_window(x, y, window=self._btn_frame, anchor="se")

        btn_style = {
            "font": ("微软雅黑", 14, "bold"),
            "width": 3,
            "bd": 0,
            "cursor": "hand2",
            "relief": "flat",
        }

        ok_btn = tk.Button(
            self._btn_frame, text="✓", bg="#00C853", fg="white",
            activebackground="#00E676", activeforeground="white",
            command=self._on_confirm, **btn_style
        )
        ok_btn.pack(side=tk.LEFT, padx=4, pady=4)

        cancel_btn = tk.Button(
            self._btn_frame, text="✕", bg="#FF1744", fg="white",
            activebackground="#FF5252", activeforeground="white",
            command=self._on_cancel_click, **btn_style
        )
        cancel_btn.pack(side=tk.LEFT, padx=4, pady=4)

    def _hide_confirm_buttons(self):
        if self._btn_frame:
            self._btn_frame.destroy()
            self._btn_frame = None

    def _on_confirm(self):
        x1, y1, x2, y2 = self._region
        self.root.destroy()
        self._save_region(x1, y1, x2, y2)

    def _on_right_click(self, event):
        self._hide_confirm_buttons()
        if self.rect_id:
            self.canvas.delete(self.rect_id)
            self.rect_id = None

    def _on_cancel_click(self):
        self.root.destroy()
        logger.info("用户取消了截屏")

    def _save_region(self, x1, y1, x2, y2):
        cropped = self.screenshot.crop((x1, y1, x2, y2))

        os.makedirs(self.save_dir, exist_ok=True)
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.jpg")
        filepath = os.path.join(self.save_dir, filename)

        try:
            cropped.convert("RGB").save(filepath, "JPEG", quality=95)
            copy_to_clipboard(cropped)
            self.result = filepath
            logger.info("区域截图已保存: %s", filepath)
            _show_toast("截屏成功")
        except Exception as e:
            logger.error("区域截图保存失败: %s", e)

    def _cancel(self):
        self.root.destroy()
        logger.info("区域截图已取消")


def capture_area(save_dir):
    selector = AreaSelector(save_dir)
    return selector.run()
