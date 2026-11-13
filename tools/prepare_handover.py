from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
def put(p,s):
    (root/p).write_text(s,encoding='utf-8')
p=root/'车机屏原型.html'
s=p.read_text(encoding='utf-8')
s=s.replace('function openModal(kind,title,desc,actions){','function openModal(kind,title,desc,actions){\n    title="演示："+title; desc="未连接车辆/后台，不会执行真实动作。以下仅为界面模拟："+desc;')
s=s.replace("t.textContent=msg;", "t.textContent='演示：未连接车辆/后台 · '+msg;")
s=s.replace('正在接通客服 13962243668','客服界面，未实际呼叫')
p.write_text(s,encoding='utf-8')
p=root/'android/app/build.gradle.kts';s=p.read_text(encoding='utf-8').replace('versionCode = 1','versionCode = 2').replace('versionName = "1.0"','versionName = "1.0.1-board1"').replace('>演示模式</div>', '>演示模式 · 未连接车辆/后台</div>');p.write_text(s,encoding='utf-8')
put('README.md','''# 鸥眸共享乘客屏
Android WebView 界面演示与设备兼容性测试；无真实车辆控制、订单核验、支付或音视频服务。模拟器结果不代表实际主板验收。

- [实际板交接入口](docs/handover/START_HERE.md)
- [开发构建](docs/development-setup.md) · [验收表](docs/acceptance.md) · [协议待确认](docs/protocol.md)
- [维护原型](车机屏原型.html) · [素材](assets/) · [Android](android/) · [变化](CHANGELOG.md)

构建：进入 android 执行 Windows `gradlew.bat assembleDebug` 或 Linux `./gradlew assembleDebug`。安装见交接入口。
最新本地 APK 位于被 Git 忽略的 deliverables；远程附件只有上传确认后才可视为已交付。不得用旧 Release 替代本次版本。
根目录 HTML 为维护源，APK HTML 由 preparePassengerAssets 生成；嵌套 my-website 副本保留但不参与构建。
''')
put('docs/handover/START_HERE.md','''# 实际板第一轮验收
本轮仅演示及兼容性测试，不需要刷机、不覆盖固件，不替换原有车机应用或系统桌面。
1. 按 [设备信息](device-info.md) 收集实际硬件资料。
2. 按 [安装更新](install-and-update.md) 核对 APK 校验值并安装。
3. 启动 com.omo.passenger，确认版本 1.0.1-board1 与演示标记。
4. 按 [验收表](../acceptance.md) 逐项操作，实际板结果默认未测。
5. 按 [反馈模板](feedback-template.md) 回传证据。

SOS、紧急停车、自检、门窗、行程、订单及支付均为模拟，不会连接车辆或后台。请勿依赖屏幕完成安全操作。
''')
put('docs/handover/device-info.md','''# 设备信息
## 已确认
工程包名 com.omo.passenger；模拟器历史环境 Android 14、1920×1200、240 dpi，仅代表模拟器。
硬件资料描述 MT6769；不能据此认定屏幕连接 RK3588。
## 待队友确认
型号、Android 版本、CPU ABI、屏幕物理及逻辑分辨率、密度、WebView 提供程序及版本、网络接入方式、ADB 可用情况：均待填。
MT6769、RK3588 与屏幕的连接关系及各自运行软件：待确认。PDF 原件及修订号待补充。
只读查询（adb 路径及 SERIAL 换成本机实际值）：
```text
adb -s SERIAL shell getprop ro.product.model
adb -s SERIAL shell getprop ro.build.version.release
adb -s SERIAL shell getprop ro.product.cpu.abilist
adb -s SERIAL shell wm size
adb -s SERIAL shell wm density
adb -s SERIAL shell dumpsys webviewupdate
adb -s SERIAL shell dumpsys connectivity
```
网络输出可能含地址信息，反馈前脱敏。不要修改设备密度。
''')
put('docs/handover/install-and-update.md','''# 安装与更新
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
''')
put('docs/handover/feedback-template.md','''# 验收反馈
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
''')
put('docs/handover/issues-and-limits.md','''# 问题与限制
|问题|影响|临时处理|负责人|
|---|---|---|---|
|实际板未验收|安装及触摸兼容性未知|按验收表实测|待定|
|系统字体回退|字形排版可能不同|人工对照截图|待定|
|UDP/MQTT 未实现|无车辆或公网业务通信|仅演示|待定|
|真实订单、支付、音视频未实现|页面状态不代表真实业务|观察演示提示|待定|
|开机自启、系统常驻、默认桌面未实现|需手动启动|后续设备联调|待定|
|MT6769/RK3588 拓扑未知|协议及部署无法确定|收集硬件资料|待定|
''')
put('docs/protocol.md','''# 协议与拓扑
需求方向：局域网 UDP 对接 RK3588，公网业务 MQTT；当前未实现。MT6769 主板、RK3588 与屏幕关系及网络拓扑未确认。
以下仅为建议草案，未经联调确认，不构成协议。

|UDP项目|状态|
|---|---|
'''+''.join('|'+x+'|待确认|\n' for x in ['运行端/IP','端口','报文结构/编码/版本','单位/范围','频率','心跳','请求编号','执行反馈','超时','重试','去重/幂等','安全校验'])+'''
|MQTT项目|状态|
|---|---|
'''+''.join('|'+x+'|待确认|\n' for x in ['运行端','Broker','TLS/证书信任','认证','Topic','消息格式/版本','发布订阅权限','QoS/保留消息/遗嘱','离线重连'])+'\n禁止提交真实密码、Token、证书私钥。\n')
put('CHANGELOG.md','''# 变更记录
## 1.0.1-board1 — 2026-11-13
- 沿用 WebView 本地资源构建及 visualViewport 等比居中修复。
- 所有弹窗和 Toast 增加未连接车辆/后台说明；保留界面流程。
- 补全设备交接、协议待确认、安装和验收资料。
- 内部 debug 测试；实际板未验收，UDP/MQTT/支付/车辆控制未实现。
''')
for name,title in [('device-acceptance','设备验收问题'),('hardware-protocol','协议或硬件资料补充')]:
    put('.github/ISSUE_TEMPLATE/'+name+'.md','---\nname: '+title+'\nabout: 记录设备信息、证据及待确认事项\ntitle: ""\nlabels: ""\nassignees: ""\n---\n\n版本/提交：\n设备与拓扑：\n复现步骤或资料来源：\n预期/实际：\n频率：\n脱敏证据：\n待确认问题：\n')
with (root/'.gitignore').open('a',encoding='utf-8') as f:f.write('\n/deliverables/\n*.apk\n*.zip\n*.jks\n*.keystore\n/build-viewport.log\n')
