plugins {
    alias(libs.plugins.android.application)
}

android {
    namespace = "com.omo.passenger"
    compileSdk {
        version = release(37)
    }

    defaultConfig {
        applicationId = "com.omo.passenger"
        minSdk = 26
        targetSdk = 37
        versionCode = 2
        versionName = "1.0.1-board1"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            optimization {
                enable = true
                packageScope = setOf("androidx.**", "kotlin.**", "kotlinx.**")
            }
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
}

dependencies {
    implementation(libs.androidx.activity.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.androidx.constraintlayout)
    implementation(libs.androidx.core.ktx)
    implementation(libs.material)
    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(libs.androidx.junit)
}
val preparePassengerAssets by tasks.registering {
    val source = rootProject.file("../车机屏原型.html")
    val images = rootProject.file("../assets")
    val output = layout.buildDirectory.dir("generated/passengerAssets")
    inputs.file(source)
    inputs.dir(images)
    outputs.dir(output)
    doLast {
        val dest = output.get().asFile
        dest.mkdirs()
        var html = source.readText(Charsets.UTF_8)
        html = html.replace("https://aka.doubaocdn.com/s/VRuaArpTM8", "assets/logo.png")
            .replace("https://aka.doubaocdn.com/s/7q93oYcqNa", "assets/car.png")
        html = html.replace(Regex("@font-face\\s*\\{[^}]*}", RegexOption.DOT_MATCHES_ALL), "")
        html = html.replace("<body>", "<body><div style='position:fixed;right:18px;top:8px;z-index:99999;background:#a33;color:white;padding:4px 12px'>演示模式 · 未连接车辆/后台</div>")
        dest.resolve("index.html").writeText(html, Charsets.UTF_8)
        images.copyRecursively(dest.resolve("assets"), overwrite = true)
    }
}
android.sourceSets["main"].assets.srcDir(layout.buildDirectory.dir("generated/passengerAssets").get().asFile)
tasks.named("preBuild") { dependsOn(preparePassengerAssets) }

dependencies { implementation("androidx.webkit:webkit:1.10.0") }


