@echo off
echo 正在安装依赖...
pip install -r requirements.txt

echo 正在打包...
pyinstaller -F -w --icon=assets/icon.ico --add-data "assets;assets" --name ScreenshotTool main.py

echo 打包完成！
echo 输出文件: dist\ScreenshotTool.exe
pause
