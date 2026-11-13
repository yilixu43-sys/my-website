# 验收反馈
- APK版本 / SHA256 / 源码提交：
- 设备型号 / Android / ABI / 分辨率 / 密度 / WebView / 网络：
- 发生时间（含时区）：
- 前置条件及复现步骤：
- 预期 / 实际 / 频率：
- 截图、视频、日志位置：

聚焦应用日志，不默认清空设备日志。先获取 PID，再替换 PID：
```text
adb -s SERIAL shell pidof com.omo.passenger
adb -s SERIAL logcat --pid=PID -d -v threadtime > passenger-log.txt
```
崩溃后 PID 可能变化，记录该限制。上传前移除订单、位置、个人信息、地址和凭据。
