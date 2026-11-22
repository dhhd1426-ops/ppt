package com.dhhd.replay;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Intent;
import android.content.res.Configuration;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.DocumentsContract;
import android.view.View;
import android.view.Window;
import android.webkit.JavascriptInterface;
import android.webkit.RenderProcessGoneDetail;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.Toast;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;

import org.json.JSONArray;
import org.json.JSONObject;

/**
 * Shows the bundled chat-replay page in a WebView.
 * The page is served from the app's assets under an https address so that its
 * on-device storage works; requests to any other host are refused.
 */
public class MainActivity extends Activity {
    private static final String HOST = "appassets.androidplatform.net";
    private static final String HOME = "https://" + HOST + "/index.html";
    private static final int PICK_FILES = 7;
    private static final int SAVE_ONE = 8;
    private static final int SAVE_FOLDER = 9;

    private WebView web;
    private ValueCallback<Uri[]> pendingFiles;
    /** Files waiting for the user to choose where to save them. */
    private String[] outNames;
    private String[] outTexts;
    private String outMime;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        buildWeb();
    }

    private boolean night() {
        int mode = getResources().getConfiguration().uiMode & Configuration.UI_MODE_NIGHT_MASK;
        return mode == Configuration.UI_MODE_NIGHT_YES;
    }

    private void applyColors() {
        boolean dark = night();
        int ground = Color.parseColor(dark ? "#1A1A18" : "#F4F2EC");
        Window w = getWindow();
        w.setStatusBarColor(ground);
        w.setNavigationBarColor(ground);
        int flags = dark ? 0 : (View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);
        w.getDecorView().setSystemUiVisibility(flags);
        if (web != null) web.setBackgroundColor(ground);
    }

    private void buildWeb() {
        web = new WebView(this);
        web.setOverScrollMode(View.OVER_SCROLL_NEVER);
        applyColors();
        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);       // imported chats are kept in IndexedDB
        s.setDatabaseEnabled(true);
        s.setAllowFileAccess(false);
        s.setTextZoom(100);
        s.setSupportZoom(false);
        web.addJavascriptInterface(new Bridge(), "NativeBridge");
        web.setWebViewClient(new Client());
        web.setWebChromeClient(new Chrome());
        setContentView(web);
        web.loadUrl(HOME);
    }

    private WebResourceResponse refused() {
        return new WebResourceResponse("text/plain", "utf-8", 404, "Not Found",
                new HashMap<String, String>(), new ByteArrayInputStream(new byte[0]));
    }

    /** The page, with the system's light or dark mode written into it. */
    private WebResourceResponse page() {
        try (InputStream in = getAssets().open("index.html")) {
            ByteArrayOutputStream buf = new ByteArrayOutputStream();
            byte[] chunk = new byte[16384];
            int n;
            while ((n = in.read(chunk)) > 0) buf.write(chunk, 0, n);
            String html = new String(buf.toByteArray(), StandardCharsets.UTF_8)
                    .replace("<html lang=\"zh-CN\">",
                            "<html lang=\"zh-CN\" data-theme=\"" + (night() ? "dark" : "light") + "\">");
            return new WebResourceResponse("text/html", "utf-8",
                    new ByteArrayInputStream(html.getBytes(StandardCharsets.UTF_8)));
        } catch (IOException e) {
            return refused();
        }
    }

    private final class Client extends WebViewClient {
        @Override
        public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
            Uri u = request.getUrl();
            String scheme = u.getScheme();
            if (!"http".equals(scheme) && !"https".equals(scheme)) return null;   // data: and blob: stay inside the page
            if (HOST.equals(u.getHost()) && "/index.html".equals(u.getPath())) return page();
            return refused();
        }

        /** Links inside a chat open in the phone's browser, never inside the app. */
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            Uri u = request.getUrl();
            if (HOST.equals(u.getHost())) return false;
            String scheme = u.getScheme();
            if ("http".equals(scheme) || "https".equals(scheme)) {
                try {
                    startActivity(new Intent(Intent.ACTION_VIEW, u));
                } catch (Exception e) {
                    Toast.makeText(MainActivity.this, "没有找到能打开链接的浏览器", Toast.LENGTH_SHORT).show();
                }
            }
            return true;
        }

        /** A very large export can exhaust the page's memory; reload instead of closing the app. */
        @Override
        public boolean onRenderProcessGone(WebView view, RenderProcessGoneDetail detail) {
            if (pendingFiles != null) { pendingFiles.onReceiveValue(null); pendingFiles = null; }
            setContentView(new View(MainActivity.this));
            view.destroy();
            buildWeb();
            Toast.makeText(MainActivity.this, "页面内存不足，已重新载入。文件太大时请只导入 conversations.json", Toast.LENGTH_LONG).show();
            return true;
        }
    }

    private final class Chrome extends WebChromeClient {
        @Override
        public boolean onShowFileChooser(WebView view, ValueCallback<Uri[]> callback, FileChooserParams params) {
            if (pendingFiles != null) pendingFiles.onReceiveValue(null);
            pendingFiles = callback;
            Intent pick = new Intent(Intent.ACTION_GET_CONTENT);
            pick.addCategory(Intent.CATEGORY_OPENABLE);
            pick.setType("*/*");
            pick.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
            try {
                startActivityForResult(Intent.createChooser(pick, "选择导出的文件"), PICK_FILES);
            } catch (Exception e) {
                pendingFiles = null;
                callback.onReceiveValue(null);
                Toast.makeText(MainActivity.this, "没有找到文件管理器", Toast.LENGTH_SHORT).show();
            }
            return true;
        }
    }

    @Override
    protected void onActivityResult(int request, int result, Intent data) {
        super.onActivityResult(request, result, data);
        if (request == SAVE_ONE || request == SAVE_FOLDER) {
            finishSave(request, result == RESULT_OK && data != null ? data.getData() : null);
            return;
        }
        if (request != PICK_FILES || pendingFiles == null) return;
        Uri[] picked = null;
        if (result == RESULT_OK && data != null) {
            ClipData clip = data.getClipData();
            if (clip != null && clip.getItemCount() > 0) {
                picked = new Uri[clip.getItemCount()];
                for (int i = 0; i < picked.length; i++) picked[i] = clip.getItemAt(i).getUri();
            } else if (data.getData() != null) {
                picked = new Uri[]{data.getData()};
            }
        }
        pendingFiles.onReceiveValue(picked);
        pendingFiles = null;
    }

    private void say(String text) {
        Toast.makeText(this, text, Toast.LENGTH_LONG).show();
    }

    /** Reads [{name, text}, ...] as sent by the page. Returns false if it is unusable. */
    private boolean takeFiles(String json, String mime) {
        try {
            JSONArray arr = new JSONArray(json);
            if (arr.length() == 0) return false;
            String[] names = new String[arr.length()];
            String[] texts = new String[arr.length()];
            for (int i = 0; i < names.length; i++) {
                JSONObject o = arr.getJSONObject(i);
                names[i] = o.getString("name").replace('/', '_');
                texts[i] = o.getString("text");
            }
            outNames = names;
            outTexts = texts;
            outMime = mime == null || mime.isEmpty() ? "text/plain" : mime;
            return true;
        } catch (Exception e) {
            return false;
        }
    }

    private void startSave(String json, String mime) {
        if (!takeFiles(json, mime)) { say("导出失败：没有读到要保存的内容"); return; }
        try {
            if (outNames.length == 1) {
                Intent one = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                one.addCategory(Intent.CATEGORY_OPENABLE);
                one.setType(outMime);
                one.putExtra(Intent.EXTRA_TITLE, outNames[0]);
                startActivityForResult(one, SAVE_ONE);
            } else {
                say("选一个文件夹，" + outNames.length + " 个文件会保存进去");
                startActivityForResult(new Intent(Intent.ACTION_OPEN_DOCUMENT_TREE), SAVE_FOLDER);
            }
        } catch (Exception e) {
            outNames = null; outTexts = null;
            say("没有找到文件管理器，可以改用“分享”");
        }
    }

    private void finishSave(final int request, final Uri where) {
        final String[] names = outNames, texts = outTexts;
        final String mime = outMime;
        outNames = null; outTexts = null;
        if (where == null) return;                       // the user backed out of the picker
        if (names == null || texts == null) { say("导出被系统中断了，请再试一次"); return; }
        new Thread(() -> {
            int done = 0;
            for (int i = 0; i < names.length; i++) {
                try {
                    Uri target = where;
                    if (request == SAVE_FOLDER) {
                        Uri dir = DocumentsContract.buildDocumentUriUsingTree(where,
                                DocumentsContract.getTreeDocumentId(where));
                        target = DocumentsContract.createDocument(getContentResolver(), dir, mime, names[i]);
                    }
                    if (target == null) continue;
                    try (OutputStream out = getContentResolver().openOutputStream(target)) {
                        if (out == null) continue;
                        out.write(texts[i].getBytes(StandardCharsets.UTF_8));
                    }
                    done++;
                } catch (Exception ignored) {
                    // counted as not saved below
                }
            }
            final int saved = done;
            runOnUiThread(() -> say(saved == names.length
                    ? "已保存 " + saved + " 个文件"
                    : "保存了 " + saved + " 个，" + (names.length - saved) + " 个没有保存成功，请换一个位置再试"));
        }).start();
    }

    private void startShare(String json, String mime) {
        if (!takeFiles(json, mime)) { say("导出失败：没有读到要分享的内容"); return; }
        final String[] names = outNames, texts = outTexts;
        outNames = null; outTexts = null;
        try {
            File dir = new File(getCacheDir(), ExportProvider.DIR);
            if (!dir.isDirectory() && !dir.mkdirs()) throw new IOException("cache");
            File[] old = dir.listFiles();
            if (old != null) for (File f : old) f.delete();
            ArrayList<Uri> uris = new ArrayList<>();
            for (int i = 0; i < names.length; i++) {
                try (FileOutputStream out = new FileOutputStream(new File(dir, names[i]))) {
                    out.write(texts[i].getBytes(StandardCharsets.UTF_8));
                }
                uris.add(ExportProvider.uriFor(names[i]));
            }
            Intent send;
            if (uris.size() == 1) {
                send = new Intent(Intent.ACTION_SEND);
                send.putExtra(Intent.EXTRA_STREAM, uris.get(0));
            } else {
                send = new Intent(Intent.ACTION_SEND_MULTIPLE);
                send.putParcelableArrayListExtra(Intent.EXTRA_STREAM, uris);
            }
            send.setType("*/*");
            ClipData clip = ClipData.newRawUri("对话", uris.get(0));
            for (int i = 1; i < uris.size(); i++) clip.addItem(new ClipData.Item(uris.get(i)));
            send.setClipData(clip);
            send.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            startActivity(Intent.createChooser(send, "分享导出的文件"));
        } catch (Exception e) {
            say("分享失败，可以改用“保存到手机”");
        }
    }

    private final class Bridge {
        @JavascriptInterface
        public void saveFiles(final String json, final String mime) {
            runOnUiThread(() -> startSave(json, mime));
        }

        @JavascriptInterface
        public void shareFiles(final String json, final String mime) {
            runOnUiThread(() -> startShare(json, mime));
        }

        @JavascriptInterface
        public void copy(final String text) {
            runOnUiThread(() -> {
                try {
                    ClipboardManager cm = (ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
                    cm.setPrimaryClip(ClipData.newPlainText("对话", text == null ? "" : text));
                } catch (Exception e) {
                    Toast.makeText(MainActivity.this, "内容太长，没能复制", Toast.LENGTH_SHORT).show();
                }
            });
        }
    }

    @Override
    public void onConfigurationChanged(Configuration config) {
        super.onConfigurationChanged(config);
        applyColors();
        if (web != null) {
            web.evaluateJavascript("document.documentElement.setAttribute('data-theme','"
                    + (night() ? "dark" : "light") + "')", null);
        }
    }

    /** Back closes the menu, the list or a selection first; with nothing open it leaves the app. */
    @Override
    public void onBackPressed() {
        if (web == null) { super.onBackPressed(); return; }
        web.evaluateJavascript("window.__appBack ? window.__appBack() : false", value -> {
            if (!"true".equals(value)) MainActivity.super.onBackPressed();
        });
    }

    @Override protected void onPause() { super.onPause(); if (web != null) web.onPause(); }
    @Override protected void onResume() { super.onResume(); if (web != null) web.onResume(); }
    @Override protected void onDestroy() { if (web != null) web.destroy(); super.onDestroy(); }
}
