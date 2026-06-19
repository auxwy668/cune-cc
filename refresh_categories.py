#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""重新生成分类页和sitemap，包含所有10篇文章"""

import os, re, glob, json

SITE_DIR = os.path.dirname(os.path.abspath(__file__))

CATEGORIES = {
    "login-spinning": {"name": "登录转圈修复", "icon": "🔄", "color": "#FF5722", "desc": "Telegram登录时持续转圈无法进入，通常是网络连接或客户端缓存问题"},
    "login-fail":     {"name": "登录失败排查", "icon": "❌", "color": "#9C27B0", "desc": "输入手机号后直接提示登录失败，或出现FLOOD_WAIT等错误代码"},
    "sms-code":       {"name": "验证码异常解决", "icon": "📩", "color": "#FF9800", "desc": "Telegram验证码短信不到、延迟、或被拦截"},
    "account-verify": {"name": "账号验证教程", "icon": "✅", "color": "#4CAF50", "desc": "从输入手机号到完成验证，新用户账号注册和验证完整流程"},
    "login-faq":      {"name": "登录常见FAQ", "icon": "❓", "color": "#2196F3", "desc": "Telegram登录过程中频繁掉线、异地登录验证、设备切换等常见疑问"},
}

ARTICLE_CATEGORY = {
    "telegram-login-spinning-fix":    "login-spinning",
    "telegram-login-fail-fix":        "login-fail",
    "telegram-sms-code-not-received": "sms-code",
    "telegram-account-verify-guide":  "account-verify",
    "telegram-login-faq":             "login-faq",
    "telegram-two-step-verification":   "account-verify",
    "telegram-login-security-tips":     "account-verify",
    "telegram-login-device-management": "login-faq",
    "telegram-session-logout-remote":   "login-faq",
    "telegram-login-timeout-fix":       "login-spinning",
}

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

def get_article_info(slug):
    fpath = os.path.join(SITE_DIR, slug + ".html")
    if not os.path.exists(fpath):
        return None
    with open(fpath, "r", encoding="utf-8-sig") as f:
        content = f.read()
    m = re.search(r'<title>(.+?) \|', content)
    title = m.group(1) if m else slug
    m = re.search(r'<meta name="description" content="(.+?)"', content)
    desc = m.group(1) if m else ""
    m = re.search(r'<h1>(.+?)</h1>', content)
    h1 = m.group(1) if m else title
    return {"slug": slug, "title": h1, "desc": desc}

def get_article_list_html(cat_slug):
    articles = []
    for slug, cat in ARTICLE_CATEGORY.items():
        if cat == cat_slug:
            info = get_article_info(slug)
            if info:
                cat_info = CATEGORIES.get(cat, {})
                info["icon"] = cat_info.get("icon", "📄")
                info["color"] = cat_info.get("color", "#666")
                articles.append(info)
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

def create_sitemap():
    urls = ["https://cune.cc/"]
    for slug in CATEGORIES:
        urls.append(f"https://cune.cc/{slug}.html")
    for slug in ARTICLE_CATEGORY:
        fpath = os.path.join(SITE_DIR, slug + ".html")
        if os.path.exists(fpath):
            urls.append(f"https://cune.cc/{slug}.html")
    for page in ["disclaimer.html", "privacy.html", "copyright.html", "contact.html"]:
        if os.path.exists(os.path.join(SITE_DIR, page)):
            urls.append(f"https://cune.cc/{page}")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for i, url in enumerate(urls):
        priority = "1.0" if i == 0 else ("0.9" if i <= 5 else "0.8")
        xml += f'  <url><loc>{url}</loc><priority>{priority}</priority><changefreq>weekly</changefreq><lastmod>2026-06-19</lastmod></url>\n'
    xml += '</urlset>\n'
    return xml

# ==================== 重新生成分类页 ====================
print("=== 重新生成分类页 ===")
for cat_slug, cat_info in CATEGORIES.items():
    cat_name = cat_info["name"]
    cat_icon = cat_info["icon"]
    cat_color = cat_info["color"]
    cat_desc = cat_info["desc"]

    article_list = get_article_list_html(cat_slug)

    faqs = {
        "login-spinning": [
            ("Telegram登录转圈多久算异常？", "正常登录验证5-10秒完成，超过30秒还在转圈基本就是连接问题。"),
            ("改了DNS还是转圈怎么办？", "换一组DNS试试，比如223.5.5.5或119.29.29.29。"),
            ("WiFi能上网但Telegram登录转圈？", "能上网不等于能连上Telegram服务器，切换到移动数据试试。"),
        ],
        "login-fail": [
            ("FLOOD_WAIT要等多久？", "FLOOD_WAIT_60就是等60秒，最长不超过24小时。"),
            ("登录失败没有错误代码？", "旧版只显示通用提示，更新到最新版会显示详细错误。"),
            ("邮件申请解封多久回复？", "通常1-7个工作日，不要频繁发邮件。"),
        ],
        "sms-code": [
            ("验证码短信一般多久能到？", "正常1-3分钟，超过5分钟建议尝试语音验证码。"),
            ("语音验证码怎么接收？", "登录页面等待2分钟后出现「语音电话接收代码」选项。"),
            ("换了手机号还能登录旧账号吗？", "需要先在旧账号设置中更换绑定的手机号。"),
        ],
        "account-verify": [
            ("新账号注册需要什么条件？", "只需要一个能接收短信或通话的手机号。"),
            ("一个手机号能注册多个账号吗？", "一个手机号同时只能绑定一个Telegram账号。"),
            ("注册后需要设置两步验证吗？", "强烈建议设置，可以防止别人用你的手机号登录。"),
        ],
        "login-faq": [
            ("为什么Telegram老是掉线？", "通常是网络不稳定导致，尝试切换网络环境。"),
            ("异地登录需要验证吗？", "从新设备或新IP登录时需要额外验证，这是正常安全机制。"),
            ("怎么查看已登录的设备？", "设置→设备，可以查看所有已登录设备并远程登出。"),
        ],
    }

    cat_faqs = faqs.get(cat_slug, [])
    faq_html = ""
    faq_schema_items = []
    for q, a in cat_faqs:
        faq_html += f'      <div class="faq-item">\n        <button class="faq-q">{q}<span class="faq-toggle">▾</span></button>\n        <div class="faq-a"><p>{a}</p></div>\n      </div>\n'
        faq_schema_items.append('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False)))

    faq_schema = '<script type="application/ld+json">\n{\n  "@context": "https://schema.org",\n  "@type": "FAQPage",\n  "mainEntity": [' + ",\n    ".join(faq_schema_items) + ']\n}\n</script>' if faq_schema_items else ""

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

    intros = {
        "login-spinning": "Telegram登录转圈是最常见的问题之一。你输入手机号后，页面就一直显示加载中，怎么都进不去。说实话这种情况大部分不是你账号的问题，而是手机端的网络设置或Telegram客户端本身需要调整。",
        "login-fail": "跟转圈不同，Telegram登录失败通常会弹出一个具体的错误提示。FLOOD_WAIT、PHONE_NUMBER_INVALID、PHONE_NUMBER_BANNED……这些英文报错代码到底什么意思？怎么解决？这个分类下面都有详细说明。",
        "sms-code": "Telegram注册和登录都需要验证码，但验证码收不到的情况太常见了——短信延迟、运营商拦截、手机号输错……这个分类帮你排查所有可能导致验证码收不到的原因。",
        "account-verify": "第一次用Telegram？不知道怎么注册账号？这个分类从下载安装到输入手机号、接收验证码、完成验证，每一步都有详细说明。还包含两步验证设置、账号安全等进阶内容。",
        "login-faq": "Telegram用着用着遇到各种奇怪问题？频繁掉线、异地登录验证、设备切换报错……这个分类汇总了Telegram登录过程中最高频的问题和解决方案。",
    }

    steps = {
        "login-spinning": [("切换网络连接", "关闭WiFi打开移动数据，或开关飞行模式10秒重置网络。"), ("修改DNS设置", "DNS改为8.8.8.8和1.1.1.1，绕过运营商DNS问题。"), ("清除Telegram缓存", "设置→应用管理→Telegram→清除缓存。"), ("更新或重装Telegram", "卸载后安装最新版本。"), ("尝试其他设备登录", "在电脑端登录排查是手机还是账号问题。")],
        "login-fail": [("识别错误代码", "查看FLOOD_WAIT/NETWORK_ERROR等报错含义。"), ("网络类错误排查", "切换网络→改DNS→清缓存→重装App。"), ("频率限制处理", "FLOOD_WAIT等待指定时间不反复重试。"), ("账号问题申诉", "PHONE_NUMBER_BANNED发邮件申请解封。"), ("格式错误修正", "确认手机号含国际区号无空格横杠。")],
        "sms-code": [("确认手机号正确", "检查国家区号和手机号是否输入正确。"), ("等待2分钟选语音验证", "登录页面等待后出现语音验证码选项。"), ("检查短信拦截", "查看手机短信拦截/垃圾箱。"), ("联系运营商", "开通国际短信接收功能。"), ("尝试其他设备接收", "验证码可能发到旧设备的Telegram上。")],
        "account-verify": [("下载安装Telegram", "从官方渠道下载全平台版本。"), ("输入手机号", "选择国家区号输入手机号点下一步。"), ("接收验证码", "短信或语音接收5位数验证码。"), ("设置个人资料", "上传头像设置昵称完成初始化。"), ("开启两步验证", "设置额外密码保护账号安全。")],
        "login-faq": [("检查网络稳定性", "频繁掉线通常是网络波动导致。"), ("查看已登录设备", "设置→设备查看并远程登出可疑设备。"), ("处理异地验证", "从新IP登录需额外验证按提示操作。"), ("设备切换注意", "换手机需重新验证手机号。"), ("联系官方支持", "无法解决的问题发邮件到recover@telegram.org。")],
    }

    cat_steps = steps.get(cat_slug, [])
    steps_html = ""
    for i, (title, desc) in enumerate(cat_steps, 1):
        steps_html += f'        <div class="gs"><div class="gs-num">{i}</div><div class="gs-text"><h4>{title}</h4><p>{desc}</p></div></div>\n'

    intro = intros.get(cat_slug, cat_desc)

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

    fpath = os.path.join(SITE_DIR, cat_slug + ".html")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(page_html)
    print(f"  ✓ {cat_slug}.html")

# 重新生成sitemap
print("\n=== 重新生成sitemap ===")
sitemap = create_sitemap()
with open(os.path.join(SITE_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap)
print(f"  ✓ sitemap.xml ({len(urls)} URLs)")

# 统计
print("\n=== 文章统计 ===")
for slug, cat in sorted(ARTICLE_CATEGORY.items(), key=lambda x: x[1]):
    info = get_article_info(slug)
    if info:
        print(f"  [{cat:20s}] {slug}.html - {info['title'][:40]}")
