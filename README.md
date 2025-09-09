### 简介

### 使用教程

### 踩坑记录

1. `pyinstaller`打包后无法显示通知，原因是`pyinstaller`无法正确寻找`win10toast`依赖。

> 在`..\Lib\site-packages\PyInstaller\hooks`中新建`hook-win10toast.py`文件，写入以下内容：
> from PyInstaller.utils.hooks import copy_metadata
> datas = copy_metadata('win10toast')

2. `pyinstaller`打包后无法返回正确的网络响应，原因是打包为无控制台的文件后，无法使用标准输入输出流。

> - 使用控制台模式打包。
> - 将代码中的`send_response`方法替换为`send_response_only`方法。