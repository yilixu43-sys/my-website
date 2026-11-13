# 设备信息
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
