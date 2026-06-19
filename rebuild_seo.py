#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cune.cc SEO重构脚本：URL语义化 + 分类页静态化 + 链接更新 + sitemap修复"""

import os
import re
import glob

SITE_DIR = os.path.dirname(os.path.abspath(__file__))

# URL映射表：旧URL → 新URL
ARTICLE_MAP = {
    "article1.html": "telegram-login-spinning-fix.html",
    "article2.html": "telegram-login-fail-fix.html",
    "article3.html": "telegram-sms-code-not-received.html",
    "article4.html": "telegram-account-verify-guide.html",
    "article5.html": "telegram-login-faq.html",
}

# 分类页映射：query参数 → 静态页面
CATEGORY_MAP = {
    "category.html?cat=spin":   "login-spinning.html",
    "category.html?cat=fail":   "login-fail.html",
    "category.html?cat=sms":    "sms-code.html",
    "category.html?cat=verify": "account-verify.html",
    "category.html?cat=faq":    "login-faq.html",
}

# 分类信息
CATEGORIES = {
    "login-spinning": {"name": "登录转圈修复", "icon": "🔄", "color": "#FF5722", "desc": "Telegram登录时持续转圈无法进入，通常是网络连接或客户端缓存问题"},
    "login-fail":     {"name": "登录失败排查", "icon": "❌", "color": "#9C27B0", "desc": "输入手机号后直接提示登录失败，或出现FLOOD_WAIT等错误代码"},
    "sms-code":       {"name": "验证码异常解决", "icon": "📩", "color": "#FF9800", "desc": "Telegram验证码短信不到、延迟、或被拦截"},
    "account-verify": {"name": "账号验证教程", "icon": "✅", "color": "#4CAF50", "desc": "从输入手机号到完成验证，新用户账号注册和验证完整流程"},
    "login-faq":      {"name": "登录常见FAQ", "icon": "❓", "color": "#2196F3", "desc": "Telegram登录过程中频繁掉线、异地登录验证、设备切换等常见疑问"},
}

# 文章对应的分类
ARTICLE_CATEGORY = {
    "telegram-login-spinning-fix":  "login-spinning",
    "telegram-login-fail-fix":      "login-fail",
    "telegram-sms-code-not-received": "sms-code",
    "telegram-account-verify-guide":  "account-verify",
    "telegram-login-faq":             "login-faq",
    # 新文章
    "telegram-two-step-verification":   "account-verify",
    "telegram-proxy-login-settings":    "login-fail",
    "telegram-login-device-management": "login-faq",
    "telegram-session-logout-remote":   "login-faq",
    "telegram-login-security-tips":     "account-verify",
}

def replace_urls(content):
    """替换所有旧URL为新URL"""
    # 先替换分类页URL（更长的pattern先替换，避免部分匹配问题）
    for old, new in CATEGORY_MAP.items():
        content = content.replace(old, new)
    # 替换文章URL
    for old, new in ARTICLE_MAP.items():
        content = content.replace(old, new)
    # 替换独立的category.html引用（不带query参数的）
    content = content.replace('href="category.html"', 'href="login-spinning.html"')
    return content

def create_redirect_page(old_name, new_name):
    """为旧URL创建301跳转页面"""
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta http-equiv="refresh" content="0;url={new_name}">
<link rel="canonical" href="https://cune.cc/{new_name}">
<title>页面已迁移</title>
</head>
<body>
<p>页面已迁移到 <a href="{new_name}">{new_name}</a></p>
<script>location.replace("{new_name}");</script>
</body>
</html>
'''

HEADER = '''<header>
<div class="container header-inner">
  <a href="index.html" class="logo"><div class="logo-icon">TG</div>TG登录报错排查</a>
  <nav>
    <a href="index.html">首页</a>
    <a href="login-spinning.html">登录转圈修复</a>
    <a href="login-fail.html">登录失败排查</a>
    <a href="sms-code.html">验证码异常</a>
    <a href="account-verify.html">账号验证教程</a>
    <a href="login-faq.html">登录FAQ</a>
  </nav>
</div>
</header>'''

FOOTER = '''<footer>
<div class="container">
  <div class="footer-grid">
    <div class="footer-brand">
      <h3>TG登录报错排查</h3>
      <p>专注解决Telegram登录转圈、登录失败、验证码异常等常见问题，提供本地设置排查方案。本站内容仅为海外合规地区软件功能科普教程，不提供网络访问相关方案，不引导任何违规操作，内容仅供学习参考。</p>
    </div>
    <div class="footer-col">
      <h4>排查分类</h4>
      <ul>
        <li><a href="login-spinning.html">登录转圈修复</a></li>
        <li><a href="login-fail.html">登录失败排查</a></li>
        <li><a href="sms-code.html">验证码异常解决</a></li>
        <li><a href="account-verify.html">账号验证教程</a></li>
        <li><a href="login-faq.html">登录常见FAQ</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>关于本站</h4>
      <ul>
        <li><a href="disclaimer.html">免责声明</a></li>
        <li><a href="privacy.html">隐私政策</a></li>
        <li><a href="copyright.html">版权声明</a></li>
        <li><a href="contact.html">联系我们</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 TG登录报错排查 · 内容仅供学习参考</span>
    <span>本站与 Telegram 官方无关</span>
  </div>
</div>
</footer>'''

STICKY_BAR = '''<div class="cpa-sticky-bar" id="cpaStickyBar">
  <div class="cpa-sticky-inner">
    <div class="cpa-sticky-info">
      <span class="cpa-sticky-name">Telegram</span>
      <span class="cpa-sticky-label">官方正版 · 安全下载</span>
    </div>
    <div class="cpa-sticky-btns">
      <a href="https://desktop.telegram.org/" target="_blank" rel="noopener" class="cpa-sticky-btn">Windows 下载</a>
      <a href="https://play.google.com/store/apps/details?id=org.telegram.messenger" target="_blank" rel="noopener" class="cpa-sticky-btn cpa-sticky-android">Android 下载</a>
      <a href="https://apps.apple.com/app/telegram-messenger/id686449807" target="_blank" rel="noopener" class="cpa-sticky-btn cpa-sticky-ios">iOS 下载</a>
    </div>
    <button class="cpa-sticky-close" onclick="document.getElementById('cpaStickyBar').style.display='none'">✕</button>
  </div>
</div>'''

CPA_CARD = '''      <div class="cpa-article-card">
        <div class="cpa-ac-head">
          <div class="cpa-ac-icon">📩</div>
          <div>
            <div class="cpa-ac-title">Telegram 官方正版下载</div>
            <div class="cpa-ac-sub">全平台支持 · 安全无捆绑 · 持续更新</div>
          </div>
        </div>
        <div class="cpa-ac-btns">
          <a href="https://desktop.telegram.org/" target="_blank" rel="noopener" class="cpa-ac-btn cpa-ac-win">🪟 Windows 下载</a>
          <a href="https://play.google.com/store/apps/details?id=org.telegram.messenger" target="_blank" rel="noopener" class="cpa-ac-btn cpa-ac-android">🤖 Android 下载</a>
          <a href="https://apps.apple.com/app/telegram-messenger/id686449807" target="_blank" rel="noopener" class="cpa-ac-btn cpa-ac-ios">🍎 iOS 下载</a>
          <a href="https://macos.telegram.org/" target="_blank" rel="noopener" class="cpa-ac-btn cpa-ac-mac">💻 macOS 下载</a>
        </div>
        <div class="cpa-ac-safe">✅ 官方正版 · 无广告捆绑 · 已通过安全认证</div>
      </div>'''

def get_article_list_html(cat_slug=None):
    """生成文章列表HTML"""
    # 收集所有文章
    articles = []
    for slug, cat in ARTICLE_CATEGORY.items():
        # 从已有的HTML文件中提取标题
        fpath = os.path.join(SITE_DIR, slug + ".html")
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8-sig") as f:
                content = f.read()
            # 提取title
            m = re.search(r'<title>(.+?)</title>', content)
            title = m.group(1) if m else slug
            # 提取description
            m = re.search(r'<meta name="description" content="(.+?)"', content)
            desc = m.group(1) if m else ""
            # 提取h1
            m = re.search(r'<h1>(.+?)</h1>', content)
            h1 = m.group(1) if m else title
            cat_info = CATEGORIES.get(cat, {})
            articles.append({
                "slug": slug,
                "cat": cat,
                "title": h1,
                "desc": desc,
                "icon": cat_info.get("icon", "📄"),
                "color": cat_info.get("color", "#666"),
            })

    # 过滤分类
    if cat_slug:
        articles = [a for a in articles if a["cat"] == cat_slug]

    html = ""
    for a in articles:
        html += f'''      <div class="article-card" style="display:flex;align-items:center;gap:20px;padding:20px">
        <div style="width:56px;height:56px;background:{a["color"]};border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px;flex-shrink:0">{a["icon"]}</div>
        <div style="flex:1">
          <h3 style="font-size:16px;margin-bottom:4px"><a href="{a["slug"]}.html">{a["title"]}</a></h3>
          <p style="font-size:13px;color:#5F6368">{a["desc"][:80]}</p>
        </div>
        <a href="{a["slug"]}.html" style="background:{a["color"]};color:#fff;padding:8px 18px;border-radius:8px;font-weight:600;font-size:13px;flex-shrink:0">阅读全文</a>
      </div>
'''
    return html

def create_category_page(cat_slug, cat_info):
    """创建静态分类页"""
    cat_name = cat_info["name"]
    cat_icon = cat_info["icon"]
    cat_color = cat_info["color"]
    cat_desc = cat_info["desc"]

    article_list = get_article_list_html(cat_slug)

    # 分类专属FAQ
    faqs = {
        "login-spinning": [
            ("Telegram登录转圈多久算异常？", "正常登录验证5-10秒完成，超过30秒还在转圈基本就是连接问题。建议先切换网络，再清除缓存重试。"),
            ("改了DNS还是转圈怎么办？", "换一组DNS试试，比如223.5.5.5（阿里DNS）或119.29.29.29（腾讯DNS）。如果所有DNS都不行，问题可能不在DNS层面。"),
            ("WiFi能上网但Telegram登录转圈？", "能上网不等于能连上Telegram服务器。部分网络环境会限制特定服务的连接，切换到移动数据试试。"),
        ],
        "login-fail": [
            ("FLOOD_WAIT要等多久？", "看具体数字。FLOOD_WAIT_60就是等60秒，FLOOD_WAIT_86400就是等24小时。最长限制一般不超过24小时。"),
            ("登录失败没有显示错误代码？", "旧版Telegram只显示通用提示。建议更新到最新版，新版本会显示更详细的错误信息。"),
            ("邮件申请解封多久回复？", "通常1-7个工作日。超过7天没回复可以再发一封，但不要频繁发。"),
        ],
        "sms-code": [
            ("验证码短信一般多久能到？", "正常情况1-3分钟内收到。超过5分钟还没到，建议尝试语音验证码。"),
            ("语音验证码怎么接收？", "登录页面等待2分钟后会出现「通过语音电话接收代码」选项，点击后Telegram会打电话念出验证码。"),
            ("换了手机号还能登录旧账号吗？", "不能直接登录。需要先用旧手机号登录，在设置中更换绑定的手机号。如果旧号已注销，需要联系Telegram官方。"),
        ],
        "account-verify": [
            ("新账号注册需要什么条件？", "只需要一个能接收短信或通话的手机号。不需要邮箱，不需要实名认证。"),
            ("一个手机号能注册多个账号吗？", "一个手机号同时只能绑定一个Telegram账号。如果要用新号注册，需要先在旧账号设置中解绑当前手机号。"),
            ("注册后需要设置两步验证吗？", "强烈建议设置。两步验证可以防止别人用你的手机号登录你的账号。"),
        ],
        "login-faq": [
            ("为什么Telegram老是掉线？", "掉线通常是网络不稳定导致。建议检查网络连接，或尝试切换WiFi/移动数据。如果问题持续，清除缓存或重装App。"),
            ("异地登录需要验证吗？", "是的，从新设备或新IP登录时，Telegram可能会要求额外验证，这是正常的安全机制。"),
            ("怎么查看已登录的设备？", "进入Telegram设置→设备，可以看到所有已登录设备的列表，可以远程登出不认识的设备。"),
        ],
    }

    cat_faqs = faqs.get(cat_slug, [])
    faq_html = ""
    faq_schema_items = []
    for q, a in cat_faqs:
        faq_html += f'''      <div class="faq-item">
        <button class="faq-q">{q}<span class="faq-toggle">▾</span></button>
        <div class="faq-a"><p>{a}</p></div>
      </div>
'''
        faq_schema_items.append(f'{{"@type":"Question","name":"{q}","acceptedAnswer":{{"@type":"Answer","text":"{a}"}}}}')

    faq_schema = ""
    if faq_schema_items:
        faq_schema = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{','.join(faq_schema_items)}]
}}
</script>'''

    breadcrumb_schema = f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{"@type":"ListItem","position":1,"name":"首页","item":"https://cune.cc/"}},
    {{"@type":"ListItem","position":2,"name":"{cat_name}","item":"https://cune.cc/{cat_slug}.html"}}
  ]
}}
</script>'''

    # 分类专属介绍内容
    intros = {
        "login-spinning": f"Telegram登录转圈是最常见的问题之一。你输入手机号后，页面就一直显示加载中，怎么都进不去。说实话这种情况大部分不是你账号的问题，而是手机端的网络设置或Telegram客户端本身需要调整。这个分类下面的教程会带你从网络连接、DNS设置、缓存清理到重装App，一步步排查。",
        "login-fail": f"跟转圈不同，Telegram登录失败通常会弹出一个具体的错误提示。FLOOD_WAIT、PHONE_NUMBER_INVALID、PHONE_NUMBER_BANNED……这些英文报错代码到底什么意思？怎么解决？这个分类下面都有详细说明。说实话，大部分报错代码一看就懂了，按照对应方法处理就行。",
        "sms-code": f"Telegram注册和登录都需要验证码，但验证码收不到的情况太常见了——短信延迟、运营商拦截、手机号输错……这个分类下面的教程会帮你排查所有可能导致验证码收不到的原因，包括语音验证码、多设备接收等替代方案。",
        "account-verify": f"第一次用Telegram？不知道怎么注册账号？这个分类从下载安装到输入手机号、接收验证码、完成验证，每一步都有详细说明。还包含两步验证设置、账号安全等进阶内容，新用户跟着做就行。",
        "login-faq": f"Telegram用着用着遇到各种奇怪问题？频繁掉线、异地登录验证、设备切换报错……这个分类汇总了Telegram登录过程中最高频的问题和解决方案，帮你快速找到答案。",
    }

    intro = intros.get(cat_slug, cat_desc)

    # 分类专属步骤
    steps = {
        "login-spinning": [
            ("切换网络连接", "关闭WiFi打开移动数据，或反过来。开关飞行模式10秒也能重置网络连接。"),
            ("修改DNS设置", "将DNS改为8.8.8.8和1.1.1.1，绕过运营商DNS的解析问题。"),
            ("清除Telegram缓存", "设置→应用管理→Telegram→存储→清除缓存（不是清除数据）。"),
            ("更新或重装Telegram", "卸载后安装最新版本，解决版本过旧导致的连接协议失效。"),
            ("尝试其他设备登录", "在电脑端登录同一账号，排查是手机端还是账号本身的问题。"),
        ],
        "login-fail": [
            ("识别错误代码", "查看报错信息，FLOOD_WAIT/NETWORK_ERROR/PHONE_NUMBER_INVALID等含义不同。"),
            ("网络类错误排查", "切换网络→改DNS→清缓存→重装App，跟转圈排查思路一致。"),
            ("频率限制处理", "FLOOD_WAIT等待指定时间，期间不要反复点击登录。"),
            ("账号问题申诉", "PHONE_NUMBER_BANNED发邮件到recover@telegram.org申请解封。"),
            ("格式错误修正", "确认手机号含国际区号（+86），无空格横杠。"),
        ],
        "sms-code": [
            ("确认手机号正确", "检查国家区号和手机号是否输入正确，尤其是国际区号。"),
            ("等待2分钟选语音验证", "登录页面等待后会出「通过语音电话接收代码」选项。"),
            ("检查短信拦截", "查看手机短信拦截/垃圾箱，部分手机会自动拦截海外短信。"),
            ("联系运营商", "部分运营商默认拦截国际短信，需开通国际短信接收功能。"),
            ("尝试其他设备接收", "如果旧设备还登录着Telegram，验证码可能发到那上面。"),
        ],
        "account-verify": [
            ("下载安装Telegram", "从官方渠道下载，支持Windows/Android/iOS/macOS全平台。"),
            ("输入手机号", "选择国家区号，输入手机号，点击下一步。"),
            ("接收验证码", "短信或语音接收5位数验证码，输入App完成验证。"),
            ("设置个人资料", "上传头像、设置昵称，完成账号初始化。"),
            ("开启两步验证", "设置→隐私→两步验证，设置额外密码保护账号安全。"),
        ],
        "login-faq": [
            ("检查网络稳定性", "频繁掉线通常是网络波动导致，尝试切换网络环境。"),
            ("查看已登录设备", "设置→设备，查看所有登录设备，远程登出可疑设备。"),
            ("处理异地验证", "从新IP登录需额外验证，这是正常安全机制，按提示操作即可。"),
            ("设备切换注意事项", "换手机登录需重新验证手机号，确保旧设备已退出登录。"),
            ("联系官方支持", "遇到无法自行解决的问题，发邮件到recover@telegram.org。"),
        ],
    }

    cat_steps = steps.get(cat_slug, [])
    steps_html = ""
    for i, (title, desc) in enumerate(cat_steps, 1):
        steps_html += f'''        <div class="gs"><div class="gs-num">{i}</div><div class="gs-text"><h4>{title}</h4><p>{desc}</p></div></div>
'''

    page_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Telegram{cat_name}教程 - TG登录报错排查 | cune.cc</title>
<meta name="description" content="{cat_desc}，提供详细的排查步骤和修复方法，覆盖Android、iOS、Windows全平台。">
<meta name="keywords" content="telegram{cat_name},TG{cat_name},telegram登录问题">
<link rel="canonical" href="https://cune.cc/{cat_slug}.html">
<link rel="stylesheet" href="css/style.css">
{faq_schema}
{breadcrumb_schema}
</head>
<body>

{HEADER}

<div class="container"><div class="breadcrumb"><a href="index.html">首页</a><span>›</span>{cat_name}</div></div>

<section class="hero" style="padding:40px 0;">
  <div class="container">
    <div class="hero-badge">{cat_icon} {cat_name}</div>
    <h1>Telegram <span>{cat_name}</span>完整解决方案</h1>
    <p class="hero-subtitle">{intro}</p>
    <div class="hero-btns">
      <a href="#guide" class="btn-primary">查看修复步骤</a>
      <a href="#faq" class="btn-secondary">常见问答</a>
    </div>
  </div>
</section>

<section class="section" id="guide" style="background:#fff;">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">修复步骤</div>
      <h2>{cat_name}排查流程</h2>
      <p class="section-sub">按顺序尝试以下方法，大多数情况可在前两步解决</p>
    </div>
    <div class="guide-grid">
      <div class="guide-steps">
{steps_html}      </div>
      <div class="guide-box">
        <h3>注意事项</h3>
        <ul>
          <li>清除缓存不会删除聊天记录，仅删除本地临时文件</li>
          <li>重新安装前请确认账号绑定的手机号可用</li>
          <li>遇到FLOOD_WAIT不要反复重试，越试等待越长</li>
          <li>修改DNS后如果其他App变慢可改回自动获取</li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section" id="articles" style="background:#fff;">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">相关教程</div>
      <h2>{cat_name}教程文章</h2>
    </div>
    <div class="articles-grid" style="grid-template-columns:1fr">
{article_list}    </div>
  </div>
</section>

<section class="section faq-section" id="faq">
  <div class="container">
    <div class="section-header">
      <div class="section-tag">常见问题</div>
      <h2>{cat_name}常见问答</h2>
    </div>
    <div class="faq-list">
{faq_html}    </div>
  </div>
</section>

<section class="cta">
  <div class="container">
    <h2>问题还没解决？</h2>
    <p>查看其他Telegram登录问题的详细教程</p>
    <div class="cta-btns">
      <a href="index.html" class="btn-white">返回首页</a>
      <a href="login-spinning.html" class="btn-outline-white">登录转圈修复</a>
    </div>
  </div>
</section>

{FOOTER}
<script src="js/main.js"></script>
</body>
</html>'''

    return page_html

def create_sitemap():
    """生成正确的sitemap.xml"""
    urls = ["https://cune.cc/"]
    # 分类页
    for slug in CATEGORIES:
        urls.append(f"https://cune.cc/{slug}.html")
    # 文章页
    for slug in ARTICLE_CATEGORY:
        fpath = os.path.join(SITE_DIR, slug + ".html")
        if os.path.exists(fpath):
            urls.append(f"https://cune.cc/{slug}.html")
    # 静态页面
    for page in ["disclaimer.html", "privacy.html", "copyright.html", "contact.html"]:
        fpath = os.path.join(SITE_DIR, page)
        if os.path.exists(fpath):
            urls.append(f"https://cune.cc/{page}")

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for i, url in enumerate(urls):
        priority = "1.0" if i == 0 else ("0.9" if i <= 5 else "0.8")
        xml += f'  <url><loc>{url}</loc><priority>{priority}</priority><changefreq>weekly</changefreq><lastmod>2026-06-19</lastmod></url>\n'
    xml += '</urlset>\n'
    return xml

def main():
    print("=== cune.cc SEO重构开始 ===\n")

    # 1. 重命名文章 + 更新链接
    print("1. 重命名文章文件...")
    for old_name, new_name in ARTICLE_MAP.items():
        old_path = os.path.join(SITE_DIR, old_name)
        new_path = os.path.join(SITE_DIR, new_name)
        if os.path.exists(old_path):
            with open(old_path, "r", encoding="utf-8-sig") as f:
                content = f.read()
            # 更新所有URL
            content = replace_urls(content)
            # 写入新文件
            with open(new_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"   ✓ {old_name} → {new_name}")
            # 为旧URL创建跳转页
            redirect = create_redirect_page(old_name, new_name)
            with open(old_path, "w", encoding="utf-8") as f:
                f.write(redirect)
            print(f"   ✓ {old_name} → 跳转页")

    # 2. 更新index.html
    print("\n2. 更新首页...")
    index_path = os.path.join(SITE_DIR, "index.html")
    with open(index_path, "r", encoding="utf-8-sig") as f:
        content = f.read()
    content = replace_urls(content)
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("   ✓ index.html 已更新")

    # 3. 更新其他HTML文件
    print("\n3. 更新其他HTML文件...")
    for fname in ["disclaimer.html", "privacy.html", "copyright.html", "contact.html"]:
        fpath = os.path.join(SITE_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8-sig") as f:
                content = f.read()
            content = replace_urls(content)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"   ✓ {fname}")

    # 4. 创建5个静态分类页
    print("\n4. 创建静态分类页...")
    for cat_slug, cat_info in CATEGORIES.items():
        page_html = create_category_page(cat_slug, cat_info)
        fpath = os.path.join(SITE_DIR, cat_slug + ".html")
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(page_html)
        print(f"   ✓ {cat_slug}.html")

    # 5. 保留旧category.html作为跳转
    print("\n5. 更新category.html跳转...")
    cat_redirect = create_redirect_page("category.html", "login-spinning.html")
    with open(os.path.join(SITE_DIR, "category.html"), "w", encoding="utf-8") as f:
        f.write(cat_redirect)
    print("   ✓ category.html → 跳转页")

    # 6. 生成sitemap
    print("\n6. 生成sitemap.xml...")
    sitemap = create_sitemap()
    with open(os.path.join(SITE_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)
    print("   ✓ sitemap.xml 已生成")

    # 7. 统计结果
    print("\n=== 重构完成 ===")
    html_files = glob.glob(os.path.join(SITE_DIR, "*.html"))
    print(f"HTML文件总数: {len(html_files)}")
    for f in sorted(html_files):
        print(f"  {os.path.basename(f)}")

if __name__ == "__main__":
    main()
