from pathlib import Path
import zipfile,hashlib,re,subprocess,json,shutil
r=Path(__file__).resolve().parents[1]
def write(p,s): (r/p).write_text(s,encoding='utf-8')
write('docs/development-setup.md','''# 开发环境
本轮实际环境 Windows PowerShell；JetBrains JDK 25、Gradle 9.6.0、AGP 9.5.1、compile/target SDK 37、min SDK 26、Build Tools 36.0.0。不升级依赖。
Windows：安装上述工具，将 JAVA_HOME 指向自己的 JDK，ANDROID_HOME 指向自己的 SDK，或在 android/local.properties 配置 sdk.dir（不提交）。进入 android 执行 `.\\gradlew.bat assembleDebug --console=plain`。
Linux 云端：本轮未运行；安装相同 JDK/SDK，配置 JAVA_HOME/ANDROID_HOME，执行 `cd android`、`chmod +x gradlew`、`./gradlew assembleDebug --console=plain`。需要访问 Google/Maven/Gradle 下载源。不能连接本地模拟器时不得声称 Android 运行通过。
维护源为根目录 车机屏原型.html 和 assets；preparePassengerAssets 在 preBuild 自动生成 app/build/generated/passengerAssets/index.html，再打包至 APK assets/index.html。修改源后重新构建安装，禁止直接维护生成文件。
两张远程图替换为本地素材，外部字体移除并使用系统回退。WebViewAssetLoader 离线加载，阻断外部请求，无 INTERNET 权限。
嵌套 my-website 副本保留，不参与本次构建。机器专属路径仅适用于原开发机，不能照抄到其他队员机器。
''')
items=['欢迎页/扫码演示/手动订单','须知逐项勾选/开始行程','仪表盘/结束行程弹窗取消确认','地图/停靠点/返回','音乐选曲/播放暂停/进度及音量滑块两端','讲解开关/暂停重播/返回','车控温度/风量/门窗/临停及恢复','SOS取消确认/客服提示','紧急停车取消确认','故障报修取消提交/自检关闭','结算/评价星级/支付/发票/重新开始','四边完整显示/居中/触摸边缘','内容滑动/滑块拖动坐标准确','断网冷启动/全部图片中文','横屏/沉浸系统栏/前台常亮10分钟','切后台再返回/系统返回键','强停再启动/设备重启后手动启动','连续运行2小时/异常和资源泄漏观察']
write('docs/acceptance.md','# 第一轮验收记录\n\n版本 1.0.1-board1；方法：静态源码与 APK 检查、Windows Gradle 构建。\n自动检查：构建通过；APK 版本、SDK、debug 签名及资源核验通过，见 handover/build-verification.json。\n本轮 adb devices 无设备，Android 安装、触摸、常亮未测。历史 viewport.png 来自此前模拟器修复，不能作为本版本通过证据。实际主板全部未测。\n\n前置条件：安装本版本、横屏、可触摸、安全静止环境；断网项目先由设备负责人关闭网络。每项记录证据文件名。\n\n|编号|前置条件|操作|预期结果|实际结果|状态|证据位置|\n|---|---|---|---|---|---|---|\n'+''.join(f'|B{i:02}|上述通用条件|{x}|显示完整、响应准确，模拟操作明确无真实执行|待填写|未测|待填写|\n' for i,x in enumerate(items,1))+'\n模拟器需独立复制此表填写，不覆盖实际板结果。开机自启、系统常驻、真实车辆动作、UDP/MQTT、真实订单支付及音视频列为待开发，不作为已通过功能。\n')
apk=r/'android/app/build/outputs/apk/debug/app-debug.apk'
with zipfile.ZipFile(apk) as z:
    html=z.read('assets/index.html').decode(); assert 'navigator.webdriver' not in html
    assert '未连接车辆/后台' in html and '@font-face' not in html
    for f in ['logo.png','car.png']:assert z.read('assets/assets/'+f)==(r/'assets'/f).read_bytes()
    native=[n for n in z.namelist() if n.startswith('lib/') and n.endswith('.so')]
    assert not re.search(r'(?:src|href)=[\"\']https?://',html)
report={'version':'1.0.1-board1','versionCode':2,'package':'com.omo.passenger','minSdk':26,'targetSdk':37,'nativeLibraries':native,'abiRestriction':'无 native 库，无 ABI 过滤；ARM 板安装仍未测','signature':'Android Debug，内部测试','checks':['assembleDebug 成功','最终 HTML 无 webdriver 分支','两张本地图片逐字节一致','最终 HTML 无外部 src/href 或字体依赖'],'androidRuntime':'本轮 adb devices 无设备，未测','board':'未测'}
write('docs/handover/build-verification.json',json.dumps(report,ensure_ascii=False,indent=2))
d=r/'deliverables';d.mkdir(exist_ok=True)
name='omo-passenger-1.0.1-board1-debug.apk';shutil.copy2(apk,d/name)
sha=hashlib.sha256((d/name).read_bytes()).hexdigest();(d/'SHA256SUMS.txt').write_text(sha+'  '+name+'\n')
notes='# 1.0.1-board1 内部测试\n界面演示及兼容性验收；未连接车辆/后台，不执行安全动作或支付。\nWindows 构建和 APK 静态核验通过；本轮无连接设备，安装、触摸、常亮、实际板均未测。\n先收集设备信息，再校验 SHA256 安装，最后按 docs/acceptance.md 反馈。无需刷机，不替换系统桌面。\n'
write('RELEASE_NOTES.md',notes);(d/'RELEASE_NOTES.md').write_text(notes,encoding='utf-8')
for p in (r/'docs').rglob('*'):
    if p.is_file():
        target=d/'docs'/p.relative_to(r/'docs');target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
print(sha)
