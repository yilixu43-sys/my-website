# 安装与更新
仅内部 debug 签名测试，minSdk 26，targetSdk 37。保留原车机应用；不设置默认桌面、开机自启或系统常驻。
先比对 SHA256SUMS.txt。文件管理器打开版本 APK，按设备设置允许该来源安装，安装完成后从应用列表启动。
ADB 路径和 SERIAL 按本机替换，先执行 adb devices 确认目标：
```text
adb -s SERIAL install -r omo-passenger-1.0.1-board1-debug.apk
adb -s SERIAL shell am start -n com.omo.passenger/.MainActivity
adb -s SERIAL shell dumpsys package com.omo.passenger
```
核对 versionName=1.0.1-board1、versionCode=2。
安装失败请保留完整错误码，记录已装版本、签名来源、设备信息。版本降级需构建更高版本；签名不一致需找回原签名或由设备负责人决定处理。不自动卸载或清数据：卸载会删除应用数据，必须先备份并明确同意。不要加 -d 掩盖版本冲突。
