package com.omo.passenger

import android.os.Bundle
import android.webkit.*
import android.view.WindowManager
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import androidx.webkit.WebViewAssetLoader
import java.io.ByteArrayInputStream

class MainActivity : AppCompatActivity() {
    private lateinit var web: WebView
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        WindowCompat.setDecorFitsSystemWindows(window, false)
        web = WebView(this)
        setContentView(web)
        web.settings.apply {
            javaScriptEnabled = true
            useWideViewPort = true
            loadWithOverviewMode = false
            allowFileAccess = false
            allowContentAccess = false
            mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
        }
        val loader = WebViewAssetLoader.Builder()
            .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(this)).build()
        web.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView, url: String) {
                view.postDelayed({
                    android.util.Log.i("Viewport", "native=" + view.width + "x" + view.height + " density=" + resources.displayMetrics.density + " padding=" + view.paddingLeft + "," + view.paddingTop)
                    view.evaluateJavascript("(function(){var r=document.getElementById('device').getBoundingClientRect(),v=visualViewport;return JSON.stringify({inner:[innerWidth,innerHeight],dpr:devicePixelRatio,visual:[v.width,v.height,v.scale],rect:[r.x,r.y,r.width,r.height]})})()") { android.util.Log.i("Viewport", it) }
                }, 1000)
            }
            override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest) = true
            override fun shouldInterceptRequest(view: WebView, request: WebResourceRequest): WebResourceResponse {
                return loader.shouldInterceptRequest(request.url)
                    ?: WebResourceResponse("text/plain", "UTF-8", 403, "Blocked", emptyMap(), ByteArrayInputStream(byteArrayOf()))
            }
        }
        web.loadUrl("https://appassets.androidplatform.net/assets/index.html")
    }
    override fun onWindowFocusChanged(hasFocus: Boolean) {
        super.onWindowFocusChanged(hasFocus)
        if (hasFocus) WindowInsetsControllerCompat(window, window.decorView).apply {
            hide(WindowInsetsCompat.Type.systemBars())
            systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
        }
    }
    override fun onDestroy() { web.destroy(); super.onDestroy() }
}


