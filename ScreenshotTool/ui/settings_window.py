import logging
import tkinter as tk
from tkinter import filedialog, messagebox

logger = logging.getLogger(__name__)


class SettingsWindow:

    def __init__(self, config, on_save=None):
        self.config = config
        self.on_save = on_save
        self.root = None

    def show(self):
        if self.root is not None and self.root.winfo_exists():
            self.root.lift()
            return

        self.root = tk.Tk()
        self.root.title("截图工具设置")
        self.root.resizable(False, False)

        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="截图快捷键:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.hotkey_entry = tk.Entry(frame, width=30)
        self.hotkey_entry.insert(0, self.config.get("hotkey", "ctrl+shift+s"))
        self.hotkey_entry.grid(row=0, column=1, pady=5, padx=(10, 0))

        tk.Label(frame, text="保存目录:").grid(row=1, column=0, sticky=tk.W, pady=5)

        dir_frame = tk.Frame(frame)
        dir_frame.grid(row=1, column=1, sticky=tk.EW, pady=5, padx=(10, 0))

        self.dir_var = tk.StringVar(value=self.config.get("save_path", ""))
        tk.Entry(dir_frame, textvariable=self.dir_var, width=22).pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Button(dir_frame, text="浏览", command=self._select_dir).pack(side=tk.RIGHT, padx=(5, 0))

        self.auto_start_var = tk.BooleanVar(value=self.config.get("auto_start", False))
        tk.Checkbutton(
            frame, text="开机自动启动", variable=self.auto_start_var
        ).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=10)

        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(10, 0))

        tk.Button(btn_frame, text="保存", command=self._save, width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="取消", command=self.root.destroy, width=10).pack(side=tk.LEFT, padx=5)

        self.root.mainloop()

    def _select_dir(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dir_var.set(folder)

    def _save(self):
        self.config["hotkey"] = self.hotkey_entry.get().strip()
        self.config["save_path"] = self.dir_var.get().strip()
        self.config["auto_start"] = self.auto_start_var.get()

        if not self.config["hotkey"]:
            messagebox.showwarning("提示", "快捷键不能为空")
            return

        if not self.config["save_path"]:
            messagebox.showwarning("提示", "请选择保存目录")
            return

        if self.on_save:
            self.on_save(self.config)

        messagebox.showinfo("提示", "设置已保存")
        self.root.destroy()
