# 鸥眸共享乘客屏
Android WebView 界面演示与设备兼容性测试；无真实车辆控制、订单核验、支付或音视频服务。模拟器结果不代表实际主板验收。

- [实际板交接入口](docs/handover/START_HERE.md)
- [开发构建](docs/development-setup.md) · [验收表](docs/acceptance.md) · [协议待确认](docs/protocol.md)
- [维护原型](车机屏原型.html) · [素材](assets/) · [Android](android/) · [变化](CHANGELOG.md)

构建：进入 android 执行 Windows `gradlew.bat assembleDebug` 或 Linux `./gradlew assembleDebug`。安装见交接入口。
最新本地 APK 位于被 Git 忽略的 deliverables；远程附件只有上传确认后才可视为已交付。不得用旧 Release 替代本次版本。
根目录 HTML 为维护源，APK HTML 由 preparePassengerAssets 生成；嵌套 my-website 副本保留但不参与构建。
