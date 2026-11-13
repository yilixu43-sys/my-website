# 开发环境
本轮实际环境 Windows PowerShell；JetBrains JDK 25、Gradle 9.6.0、AGP 9.5.1、compile/target SDK 37、min SDK 26、Build Tools 36.0.0。不升级依赖。
Windows：安装上述工具，将 JAVA_HOME 指向自己的 JDK，ANDROID_HOME 指向自己的 SDK，或在 android/local.properties 配置 sdk.dir（不提交）。进入 android 执行 `.\gradlew.bat assembleDebug --console=plain`。
Linux 云端：本轮未运行；安装相同 JDK/SDK，配置 JAVA_HOME/ANDROID_HOME，执行 `cd android`、`chmod +x gradlew`、`./gradlew assembleDebug --console=plain`。需要访问 Google/Maven/Gradle 下载源。不能连接本地模拟器时不得声称 Android 运行通过。
维护源为根目录 车机屏原型.html 和 assets；preparePassengerAssets 在 preBuild 自动生成 app/build/generated/passengerAssets/index.html，再打包至 APK assets/index.html。修改源后重新构建安装，禁止直接维护生成文件。
两张远程图替换为本地素材，外部字体移除并使用系统回退。WebViewAssetLoader 离线加载，阻断外部请求，无 INTERNET 权限。
嵌套 my-website 副本保留，不参与本次构建。机器专属路径仅适用于原开发机，不能照抄到其他队员机器。
