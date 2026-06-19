#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为cune.cc批量生成新文章HTML"""

import os
import json

SITE_DIR = os.path.dirname(os.path.abspath(__file__))

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
      <p>专注解决Telegram登录转圈、登录失败、验证码异常等常见问题。本站与 Telegram 官方无关，内容仅供学习参考。</p>
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

def build_article(slug, title, cat_name, cat_url, desc, kw, body_html, faq_items, related_links):
    """生成完整文章HTML"""
    # FAQ Schema
    faq_schema_items = []
    for q, a in faq_items:
        faq_schema_items.append('{"@type":"Question","name":%s,"acceptedAnswer":{"@type":"Answer","text":%s}}' % (
            json.dumps(q, ensure_ascii=False), json.dumps(a, ensure_ascii=False)
        ))
    faq_schema = ""
    if faq_schema_items:
        faq_schema = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [%s]
}
</script>''' % ",\n    ".join(faq_schema_items)

    # Breadcrumb Schema
    breadcrumb_schema = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type":"ListItem","position":1,"name":"首页","item":"https://cune.cc/"},
    {"@type":"ListItem","position":2,"name":"%s","item":"https://cune.cc/%s"},
    {"@type":"ListItem","position":3,"name":"%s","item":"https://cune.cc/%s.html"}
  ]
}
</script>''' % (cat_name, cat_url, title, slug)

    # FAQ HTML
    faq_html = ""
    for q, a in faq_items:
        faq_html += '''      <div class="faq-item">
        <button class="faq-q">%s<span class="faq-toggle">▾</span></button>
        <div class="faq-a"><p>%s</p></div>
      </div>
''' % (q, a)

    # Related links HTML
    related_html = ""
    for link_url, link_text in related_links:
        related_html += '          <li><a href="%s">%s</a></li>\n' % (link_url, link_text)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | TG登录排查</title>
<meta name="description" content="{desc}">
<meta name="keywords" content="{kw}">
<link rel="canonical" href="https://cune.cc/{slug}.html">
<link rel="stylesheet" href="css/style.css">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title}",
  "description": "{desc}",
  "datePublished": "2026-06-19",
  "dateModified": "2026-06-19",
  "author": {{"@type": "Organization", "name": "TG登录报错排查"}}
}}
</script>
{faq_schema}
{breadcrumb_schema}
</head>
<body>

{HEADER}

<div class="container">
  <div class="breadcrumb">
    <a href="index.html">首页</a><span>›</span><a href="{cat_url}">{cat_name}</a><span>›</span>{title}
  </div>
</div>

<section class="section">
  <div class="container" style="max-width:800px">
    <article>
      <h1>{title}</h1>
      <div style="color:#5F6368;font-size:14px;margin-bottom:28px">
        <span>分类：{cat_name}</span> · <span>更新：2026年6月19日</span>
      </div>

{body_html}

      <div style="background:#FFF3E0;border-left:4px solid #FF9800;padding:16px 20px;border-radius:0 8px 8px 0;margin:28px 0;font-size:14px;color:#5F6368">
        <strong>📌 免责声明：</strong>本站内容仅为海外合规地区软件功能科普教程，不提供网络访问相关方案，不引导任何违规操作，内容仅供学习参考。
      </div>

{CPA_CARD}

      <div style="margin-top:36px;padding-top:24px;border-top:1px solid #e8eaed">
        <h3>相关教程</h3>
        <ul style="margin:12px 0 0 20px;line-height:2.2">
{related_html}        </ul>
      </div>
    </article>
  </div>
</section>

{FOOTER}
{STICKY_BAR}
<script src="js/main.js"></script>
</body>
</html>'''

    return html

# ==================== 文章1: 两步验证 ====================
article1_body = '''      <p style="font-size:17px;line-height:1.9;color:#3C4043;margin-bottom:24px">说实话，用Telegram这么久，我一直是那种"验证码登录就够了"的心态。直到有一天朋友的号被人盗了，聊天记录全被翻出来，我才意识到两步验证这东西不是可选项，是刚需。这篇文章就手把手教你设置Telegram两步验证，从设密码到绑邮箱，一步不落。</p>

      <h2>为什么一定要开两步验证</h2>
      <p>Telegram默认的登录方式是手机号+验证码。也就是说，谁拿到了你的手机号并且能收到验证码，就能登录你的账号。想想看，如果你的手机号被SIM卡劫持，或者验证码短信被拦截，账号就没了。</p>
      <p>两步验证就是在验证码之外再加一道密码。即使别人拿到了你的验证码，没有这个密码也登不进去。说白了就是给你的账号加了一把锁，钥匙只有你自己有。如果你还不了解Telegram账号注册流程，可以先看看<a href="telegram-account-verify-guide.html">Telegram新账号验证完整操作步骤</a>。</p>

      <h2>设置两步验证的完整步骤</h2>

      <h3>第一步：进入隐私设置</h3>
      <p>打开Telegram，点右下角「设置」（iOS）或左上角菜单→「设置」（Android），找到「隐私」选项，点进去后你会看到「两步验证」这个选项。</p>
      <p>如果你之前从没设置过，它会显示"已停用"。点进去，系统会提示你设置一个密码。</p>

      <h3>第二步：设置恢复密码</h3>
      <p>这里要特别注意：你设置的密码<strong>Telegram服务器是不会存储明文的</strong>，也就是说如果你忘了，Telegram官方也帮不了你找回。所以一定要设一个自己记得住，别人猜不到的密码。</p>
      <p>建议用密码管理器生成一个强密码，然后存起来。千万别用生日、手机号这种容易被猜到的。</p>

      <h3>第三步：设置恢复邮箱</h3>
      <p>这一步非常关键。设置密码后，系统会提示你绑定一个恢复邮箱。如果你忘了密码，可以通过这个邮箱重置。讲真，这步一定不能跳过，不然密码忘了就只能<a href="https://telegram.org" target="_blank" rel="noopener">重新注册</a>了。</p>
      <p>输入邮箱地址后，Telegram会发一封验证邮件到你邮箱，点开邮件里的链接确认就完成了。</p>

      <h3>第四步：确认设置</h3>
      <p>最后系统会让你再输一次刚才设的密码确认。确认后，两步验证就正式开启了。以后在新设备上登录Telegram，除了验证码还需要输入这个密码。</p>

      <h2>忘记两步验证密码怎么办</h2>
      <p>这是被问得最多的问题。如果你设了恢复邮箱，事情就好办：</p>
      <p>在登录页面输入验证码后，系统会要求输入两步验证密码。这时候点「忘记密码」，Telegram会把重置链接发到你绑定的恢复邮箱。去邮箱点链接就能重置密码了。</p>
      <p>但如果你当时没设恢复邮箱……那就比较麻烦了。你唯一的选择是等待7天，7天后Telegram会允许你通过手机号验证码重置账号。但这7天内你完全无法使用这个账号。而且重置后，原有的云聊天记录会全部丢失。所以再说一遍，<strong>恢复邮箱一定要设</strong>。</p>

      <h2>两步验证的注意事项</h2>
      <ul style="margin:12px 0 20px 20px;line-height:2;color:#3C4043">
        <li>密码至少8位，建议包含大小写字母+数字+符号</li>
        <li>恢复邮箱建议用常用邮箱，别用临时邮箱</li>
        <li>换手机后登录需要输入两步验证密码，提前记好</li>
        <li>两步验证密码和Telegram账号密码是两回事，别搞混</li>
        <li>如果怀疑密码泄露，可以在设置里随时修改</li>
      </ul>

      <p>设置完两步验证后，建议再看看<a href="telegram-login-security-tips.html">Telegram登录安全技巧</a>，里面还有几个保护账号的小招数。另外如果你在登录时就遇到了问题，比如一直转圈，可以先去<a href="login-spinning.html">登录转圈修复分类</a>找对应方案。</p>
'''

article1_faqs = [
    ("两步验证密码忘了，没有设恢复邮箱怎么办？", "只能等待7天重置。7天后可以通过手机号验证码重置账号，但云聊天记录会全部丢失。这就是为什么一定要设恢复邮箱。"),
    ("两步验证密码可以和Telegram登录密码一样吗？", "Telegram没有「登录密码」的概念，登录靠的是手机号+验证码。两步验证密码是你额外设置的第二层密码，两者不是一回事。"),
    ("开了两步验证后每次登录都要输密码吗？", "不需要。同一个设备登录过一次后，Telegram会记住这个设备。只有在新设备上首次登录时才需要输入两步验证密码。"),
    ("两步验证密码能修改吗？", "可以。进入设置→隐私→两步验证→修改密码，输入旧密码后就能设置新密码。建议每3-6个月换一次。"),
]

# ==================== 文章2: 登录安全技巧 ====================
article2_body = '''      <p style="font-size:17px;line-height:1.9;color:#3C4043;margin-bottom:24px">很多人觉得Telegram用着挺安全的，毕竟消息是加密的嘛。但说实话，账号安全这块你不能光靠Telegram，自己也得上点心。这篇文章整理了几个实用的Telegram登录安全技巧，都是我踩过坑总结出来的，希望能帮你少走弯路。</p>

      <h2>一、一定开两步验证</h2>
      <p>这个我说多少遍都不嫌多。两步验证是你账号安全的基石，没有这个，别人拿到你手机号+验证码就能登你账号。具体的设置方法我专门写了篇<a href="telegram-two-step-verification.html">两步验证设置教程</a>，跟着做就行，5分钟搞定。</p>
      <p>核心逻辑很简单：验证码是"你有什么"（手机），两步验证密码是"你知道什么"（密码）。两层保护叠加，安全性直接翻倍。</p>

      <h2>二、定期检查已登录设备</h2>
      <p>Telegram支持多设备同时登录，这很方便，但也意味着如果有人偷偷登了你的号，你不一定能马上发现。建议每周检查一次已登录设备列表。</p>
      <p>操作路径：设置→设备。这里会列出所有登录你账号的设备，包括设备型号、登录位置和最后活跃时间。看到不认识的设备？赶紧点「终止会话」踢掉它。详细的设备管理方法可以看<a href="telegram-login-device-management.html">设备管理教程</a>。</p>

      <h2>三、谨慎使用第三方客户端</h2>
      <p>Telegram官方开放了API，所以市面上有很多第三方Telegram客户端。有些确实做得不错，功能比官方还多。但风险在于：第三方客户端的安全性你没法保证，有些甚至会偷偷记录你的登录凭证。</p>
      <p>建议：日常使用就用官方客户端。如果一定要用第三方，选择开源的、社区口碑好的，比如Nekogram、Plus Messenger这种。来路不明的客户端绝对不要装。</p>
      <p>官方客户端下载地址可以看我们首页的<a href="index.html">TG登录排查首页</a>，有各平台官方下载链接。</p>

      <h2>四、别在公共WiFi下登录</h2>
      <p>公共WiFi的安全性基本等于零。黑客可以在同一个WiFi下截获你的网络数据，包括Telegram登录请求。虽然Telegram本身有加密，但在不安全的网络环境下，风险总是存在的。</p>
      <p>如果必须用公共WiFi，至少做到：不登录新设备、不进行敏感操作（如修改密码、绑定邮箱）。用完即走，别挂着不关。</p>

      <h2>五、开启登录通知</h2>
      <p>Telegram默认会在新设备登录时给你发通知，这个功能一定要保持开启。如果突然收到"新设备登录"的通知但你没操作，立刻去设置→设备里把那个设备踢掉，然后修改两步验证密码。</p>
      <p>有些人会关掉这个通知觉得烦，讲真这是因小失大。安全通知就像烟雾报警器，平时觉得吵，关键时刻能救命。</p>

      <h2>六、设置强密码并定期更换</h2>
      <p>两步验证密码的强度直接决定账号安全。一个好密码的标准：</p>
      <ul style="margin:12px 0 20px 20px;line-height:2;color:#3C4043">
        <li>至少12位字符</li>
        <li>包含大写字母、小写字母、数字、特殊符号</li>
        <li>不用生日、手机号、姓名拼音等可推断信息</li>
        <li>不和其他平台密码重复</li>
        <li>每3-6个月更换一次</li>
      </ul>
      <p>记不住？用密码管理器。Bitwarden、1Password、KeePass都行，选一个用起来顺手的。</p>

      <h2>七、小心钓鱼链接</h2>
      <p>Telegram里经常有人发各种链接，有些伪装得跟Telegram官方登录页面一模一样，你一输入手机号和验证码，账号就没了。</p>
      <p>判断方法：Telegram官方永远不会通过聊天消息让你"验证账号"或"重新登录"。看到这类消息直接举报+拉黑。如果你在登录环节遇到问题，比如<a href="telegram-login-fail-fix.html">登录失败报错</a>，先到我们网站找解决方案，别乱点链接。</p>

      <p>以上7条技巧做到位，你的Telegram账号安全水平就超过90%的用户了。安全这东西就是这样，你多花5分钟设置，可能避免的是不可挽回的损失。如果你还想了解更多登录问题排查，可以去<a href="login-faq.html">登录FAQ分类</a>逛逛。</p>
'''

article2_faqs = [
    ("Telegram账号被盗了怎么找回？", "立即在另一台设备登录（需两步验证密码），然后去设置→设备踢掉可疑设备。如果无法登录，联系 recover@telegram.org 申请找回。"),
    ("两步验证开了但觉得每次输密码麻烦怎么办？", "同一设备只需输入一次。如果实在觉得麻烦，可以用密码管理器自动填充，不要为了方便关闭两步验证。"),
    ("怎么知道有没有人偷偷登录我的账号？", "设置→设备，查看所有已登录设备。如果有不认识的设备或异常登录位置，立即终止该会话并修改密码。"),
    ("第三方Telegram客户端安全吗？", "开源的知名客户端（如Nekogram）相对安全，但来路不明的客户端绝对不要用，可能窃取登录凭证。"),
]

# ==================== 文章3: 设备管理 ====================
article3_body = '''      <p style="font-size:17px;line-height:1.9;color:#3C4043;margin-bottom:24px">Telegram有个特别实用的功能——多设备同时登录。手机、电脑、平板可以一起用，消息自动同步。但问题来了：你登录过多少台设备？有没有在别人电脑上登过忘了退？今天就来教你查看和管理所有已登录设备，把不安全的会话统统踢掉。</p>

      <h2>查看已登录设备列表</h2>
      <p>操作很简单，不同平台路径略有不同：</p>
      <p><strong>手机端</strong>：打开Telegram→设置→设备（iOS叫"设备"，Android叫"设备/会话"）</p>
      <p><strong>电脑端</strong>：设置→设备→活跃会话</p>
      <p>进去后你会看到一个列表，显示每个设备的：</p>
      <ul style="margin:12px 0 20px 20px;line-height:2;color:#3C4043">
        <li>设备型号（如iPhone 15 Pro、Windows PC）</li>
        <li>应用名称和版本</li>
        <li>登录位置（城市级别）</li>
        <li>最后活跃时间</li>
        <li>IP地址</li>
      </ul>
      <p>说实话，第一次看这个列表的时候我吓了一跳——3台旧手机、2台公共电脑，全都还登着。赶紧全给踢了。</p>

      <h2>远程退出单个设备</h2>
      <p>看到不认识或者不再使用的设备，点它，然后选「终止会话」。这个设备会立刻被退出登录，不能再访问你的账号。</p>
      <p>如果你怀疑某个设备是被盗号登录的，除了终止会话，建议还要：</p>
      <ul style="margin:12px 0 20px 20px;line-height:2;color:#3C4043">
        <li>修改两步验证密码（设置→隐私→两步验证→修改密码）</li>
        <li>检查是否有可疑的消息转发规则</li>
        <li>查看最近聊天记录有没有异常</li>
      </ul>

      <h2>一键退出所有其他设备</h2>
      <p>如果你觉得一个一个踢太麻烦，Telegram提供了"一键退出所有其他设备"的功能。在设备列表页面，最下方有个「终止所有其他会话」按钮。</p>
      <p>点了之后，除了你当前正在用的这台设备，其他全部会被踢下线。适合在怀疑账号被盗时紧急使用。</p>
      <p>不过要注意，被踢的设备想重新登录需要验证码+两步验证密码。如果你还没开两步验证，赶紧去<a href="telegram-two-step-verification.html">设置两步验证</a>，不然这个功能等于白用。</p>

      <h2>多设备登录的限制</h2>
      <p>Telegram的多设备登录数量是有限制的：</p>
      <ul style="margin:12px 0 20px 20px;line-height:2;color:#3C4043">
        <li>主设备（手机）只能有1台</li>
        <li>同时连接的设备最多4台</li>
        <li>已配对的设备总数可以更多，但同时活跃的不能超过4台</li>
      </ul>
      <p>超过限制时，Telegram会自动把最早登录的设备设为非活跃。如果你需要登录新设备但已达上限，需要先退出一个旧设备。</p>

      <h2>设备安全自查清单</h2>
      <p>建议每个月做一次设备安全自查：</p>
      <ul style="margin:12px 0 20px 20px;line-height:2;color:#3C4043">
        <li>查看设备列表，确认没有陌生设备</li>
        <li>检查最后活跃时间，有没有异常时段的登录</li>
        <li>确认登录位置和你实际所在地一致</li>
        <li>删除不再使用的旧设备会话</li>
        <li>确认两步验证处于开启状态</li>
      </ul>
      <p>如果你发现设备列表里有从没去过的城市的登录记录，那大概率是账号被人试过了。立刻终止那个会话，然后去<a href="telegram-login-security-tips.html">登录安全技巧</a>看看还需要做哪些防护。另外如果你在登录时遇到问题，比如<a href="telegram-login-spinning-fix.html">登录一直转圈</a>，也可以在设备管理这里检查是不是会话冲突导致的。</p>

      <p>设备管理这事儿说大不大说小不小，但养成定期检查的习惯，至少能让你在账号出问题之前发现端倪。如果你还需要了解更多登录相关的问题，可以去<a href="login-faq.html">登录FAQ分类页</a>看看。</p>
'''

article3_faqs = [
    ("终止会话后那台设备还能看到我的聊天记录吗？", "不能。终止会话后设备会立刻退出登录，无法再访问你的账号。但该设备之前下载到本地的媒体文件可能还在。"),
    ("为什么设备列表里有我没用过的设备？", "可能是你之前借别人电脑登录过忘了退，也可能是账号被试过密码。如果确认不是自己登录的，立即终止会话并修改密码。"),
    ("换手机后旧手机的Telegram需要手动退出吗？", "建议手动退出。虽然可以在新设备上远程终止旧设备会话，但最安全的方式是在旧手机上直接退出登录。"),
    ("最多能同时登录几台设备？", "同时活跃设备最多4台（含手机主设备），但已配对设备总数可以更多。超过4台同时活跃时，最早的会被设为非活跃。"),
]

# ==================== 文章4: 远程登出 ====================
article4_body = '''      <p style="font-size:17px;line-height:1.9;color:#3C4043;margin-bottom:24px">你有没有过这种经历：在公司电脑上登了Telegram，下班忘了退；去打印店用公共电脑登了一下，走的时候没退出。这种情况下你的账号就一直挂在那台设备上，谁都能看到你的聊天。今天就教你几种远程登出的方法，不管你在哪，都能把不安全的设备踢下线。</p>

      <h2>方法一：通过Telegram App远程登出</h2>
      <p>这是最直接的方法。打开你手机上的Telegram，进入设置→设备，你会看到所有已登录设备列表。找到要退出的那台设备，点击它，然后选「终止会话」。</p>
      <p>操作就两步，非常简单。被终止的设备会立刻断开连接，无法再收发消息。如果你想一次性退出所有设备，点页面底部的「终止所有其他会话」就行。</p>
      <p>更详细的操作步骤可以看<a href="telegram-login-device-management.html">设备管理教程</a>，里面有截图说明。</p>

      <h2>方法二：修改密码触发全设备登出</h2>
      <p>如果你怀疑账号被盗了，光踢设备可能不够，因为对方可能在你的设备列表被刷新前还有操作窗口。这时候可以修改两步验证密码。</p>
      <p>修改密码后，所有其他设备会在下次需要验证时被要求输入新密码。如果对方不知道新密码，就登不进来了。</p>
      <p>操作路径：设置→隐私→两步验证→修改密码。如果你还没开两步验证，赶紧去<a href="telegram-two-step-verification.html">设置两步验证</a>。</p>

      <h2>方法三：通过Telegram网页版操作</h2>
      <p>如果你的手机不在身边，但有电脑可以上网，可以通过Telegram Web来管理设备：</p>
      <p>打开 web.telegram.org，登录你的账号，然后进入设置→设备，操作和手机端一样。</p>
      <p>不过要注意，用网页版本身就会创建一个新会话。操作完记得把自己这台电脑的会话也退掉。</p>

      <h2>什么情况下需要紧急远程登出</h2>
      <p>以下几种情况建议立即远程登出所有设备：</p>
      <ul style="margin:12px 0 20px 20px;line-height:2;color:#3C4043">
        <li>收到"新设备登录"通知但你没操作</li>
        <li>发现聊天记录有不是自己发的消息</li>
        <li>设备列表出现不认识的设备</li>
        <li>手机丢失或被盗</li>
        <li>在公共设备上登录过但不确定是否退出</li>
      </ul>
      <p>如果是手机丢失的情况，除了远程登出，还建议联系运营商挂失SIM卡，防止别人用你的手机号接收验证码。这也是为什么我们一直强调要开两步验证——即使手机丢了，对方没有两步验证密码也登不进你的Telegram。更多安全建议可以看<a href="telegram-login-security-tips.html">登录安全技巧</a>。</p>

      <h2>远程登出后的影响</h2>
      <p>远程登出某个设备后，那台设备上：</p>
      <ul style="margin:12px 0 20px 20px;line-height:2;color:#3C4043">
        <li>无法收发新消息</li>
        <li>无法查看新消息（已经加载到本地的仍可看到）</li>
        <li>无法使用任何账号功能</li>
        <li>如果想重新登录需要验证码+两步验证密码</li>
      </ul>
      <p>对你的主设备（手机）和其他正常设备没有任何影响，消息照常收发。</p>

      <h2>防止忘记退出的小技巧</h2>
      <p>与其每次忘退了再远程踢，不如养成好习惯：</p>
      <ul style="margin:12px 0 20px 20px;line-height:2;color:#3C4043">
        <li>在公共设备上登录后，设置提醒自己退出</li>
        <li>每周检查一次设备列表，及时清理</li>
        <li>开启两步验证，即使忘退出别人也进不去</li>
        <li>不用Telegram Web版在公共电脑登录</li>
      </ul>
      <p>如果你在登录环节遇到问题导致无法远程操作，比如<a href="telegram-login-fail-fix.html">登录失败</a>或<a href="telegram-login-spinning-fix.html">登录一直转圈</a>，可以先到对应的教程页找解决方案。更多登录相关的问题也可以去<a href="login-faq.html">登录FAQ</a>看看。</p>
'''

article4_faqs = [
    ("远程登出后对方会收到通知吗？", "不会。被终止会话的设备只是突然断开连接，不会收到任何通知。对方只会发现Telegram突然要求重新登录。"),
    ("终止所有会话包括当前设备吗？", "不包括。「终止所有其他会话」只会退出除当前设备以外的所有设备，你正在操作的设备不受影响。"),
    ("手机丢了怎么保护Telegram账号？", "立即用其他设备登录Telegram，终止丢失手机上的会话。然后联系运营商挂失SIM卡，防止验证码被接收。如果开了两步验证，对方没有密码也登不进去。"),
    ("远程登出后本地聊天记录还在吗？", "在。远程登出只断开网络连接，设备上已下载到本地的消息和文件不会被删除。但新消息不会再同步到该设备。"),
]

# ==================== 文章5: 登录超时 ====================
article5_body = '''      <p style="font-size:17px;line-height:1.9;color:#3C4043;margin-bottom:24px">Telegram登录时一直转圈，等了半天最后弹出一个"超时"或"TIMEOUT"错误？这种情况比纯粹的转圈更让人崩溃，因为你等了那么久，结果还是失败了。别急，今天就把Telegram登录超时的所有原因和修复方法给你讲清楚。</p>

      <h2>登录超时是什么意思</h2>
      <p>简单说就是你的手机向Telegram服务器发送了登录请求，但服务器在规定时间内没有回应。就像你打电话对方一直不接，等了30秒你就挂了——这就是超时。</p>
      <p>超时和转圈其实是一个问题的不同阶段：先是转圈（正在尝试连接），然后超时（连接失败，放弃）。所以很多排查方法是通用的，如果你还没看过<a href="telegram-login-spinning-fix.html">登录转圈修复教程</a>，建议先看一下。</p>

      <h2>原因一：网络连接不稳定</h2>
      <p>这是最常见的原因。WiFi信号弱、移动数据在地下室/电梯里没信号、网络延迟过高，都会导致登录请求在传输过程中超时。</p>
      <p><strong>排查方法</strong>：</p>
      <ul style="margin:12px 0 20px 20px;line-height:2;color:#3C4043">
        <li>打开浏览器试试能不能正常加载网页</li>
        <li>切换WiFi和移动数据，看哪种网络能登录</li>
        <li>开关飞行模式10秒，重置网络连接</li>
        <li>如果用WiFi，靠近路由器再试</li>
      </ul>
      <p>说实话，大部分登录超时换个网络就好了。我之前在公司WiFi下怎么都登不上，切到移动数据秒登。</p>

      <h2>原因二：DNS解析问题</h2>
      <p>你的手机需要通过DNS把Telegram的服务器域名解析成IP地址，如果DNS响应慢或解析失败，登录就会超时。</p>
      <p><strong>修复方法</strong>：手动修改DNS为公共DNS</p>
      <p>Android：设置→WiFi→长按当前网络→修改网络→高级选项→IP设置改"静态"→DNS1填<code>8.8.8.8</code>，DNS2填<code>1.1.1.1</code></p>
      <p>iOS：设置→WiFi→点当前网络右侧"i"→配置DNS→手动→添加<code>8.8.8.8</code>和<code>1.1.1.1</code></p>
      <p>改完后重新打开Telegram登录试试。如果还不行，换一组DNS：<code>223.5.5.5</code>（阿里）或<code>119.29.29.29</code>（腾讯）。</p>

      <h2>原因三：Telegram服务端故障</h2>
      <p>有时候不是你的问题，是Telegram服务器自己挂了。这种情况通常是大面积故障，你可以去社交媒体搜一下"Telegram down"看看有没有其他人也在反馈。</p>
      <p>如果是服务端故障，你只能等。一般几十分钟到几小时就会恢复。期间不要反复尝试登录，否则可能触发FLOOD_WAIT限制，到时候服务器恢复了你也登不了。关于FLOOD_WAIT的详细说明可以看<a href="telegram-login-fail-fix.html">登录失败排查教程</a>。</p>

      <h2>原因四：客户端版本过旧</h2>
      <p>Telegram会不定期更新连接协议，旧版本可能使用了已废弃的连接方式，导致无法和服务器正常通信。这时候的表现就是：能上网，DNS也正常，但登录就是超时。</p>
      <p><strong>解决方法</strong>：去应用商店更新到最新版Telegram。如果商店里没有更新，卸载后从官方渠道重新安装。官方下载链接可以在我们<a href="index.html">首页</a>找到。</p>

      <h2>原因五：系统时间不正确</h2>
      <p>这个原因很多人想不到。Telegram登录使用TLS加密，TLS证书验证依赖系统时间。如果你的手机时间偏差太大（比如电池没电导致时间重置），证书验证会失败，连接就超时了。</p>
      <p><strong>检查方法</strong>：设置→日期与时间→开启"自动设置"。确保时间和时区都正确。</p>

      <h2>快速排查流程</h2>
      <p>遇到登录超时，按这个顺序排查，通常前两步就能解决：</p>
      <ul style="margin:12px 0 20px 20px;line-height:2;color:#3C4043">
        <li>切换网络（WiFi↔移动数据）→ 60%的情况这步就解决了</li>
        <li>修改DNS为8.8.8.8 → 再解决20%</li>
        <li>检查系统时间是否自动 → 再解决10%</li>
        <li>更新/重装Telegram → 再解决5%</li>
        <li>等待服务端恢复 → 最后5%</li>
      </ul>

      <p>如果你试了以上所有方法还是超时，可以在<a href="login-spinning.html">登录转圈分类</a>看看更多排查方案，或者去<a href="login-faq.html">登录FAQ</a>找找有没有类似情况的解答。有时候问题可能出在验证码环节，那可以看看<a href="telegram-sms-code-not-received.html">收不到验证码</a>的解决方法。</p>
'''

article5_faqs = [
    ("登录超时和登录转圈是一回事吗？", "不完全是。转圈是正在尝试连接的过程，超时是连接尝试失败后的结果。超时通常发生在转圈一段时间（通常是30秒）之后。"),
    ("为什么换了网络还是超时？", "可能是DNS问题，试试修改DNS为8.8.8.8。也可能是客户端版本过旧或系统时间不正确，逐一排查。"),
    ("登录超时会一直持续吗？", "不会。如果是网络问题，换网络就能解决。如果是服务端故障，等几小时就恢复了。反复尝试登录可能触发FLOOD_WAIT限制。"),
    ("超时后需要等多久才能重新登录？", "不需要额外等待。确认网络正常后就可以重新尝试登录。但如果触发了FLOOD_WAIT，需要等指定秒数后才能重试。"),
]

# ==================== 生成所有文章 ====================
articles = [
    {
        "slug": "telegram-two-step-verification",
        "title": "Telegram两步验证怎么设置？手把手教你给账号加把锁",
        "cat_name": "账号验证教程",
        "cat_url": "account-verify.html",
        "desc": "Telegram两步验证设置完整教程，从设置密码到邮箱恢复，一步步教你给账号加一层安全保护，防止被盗号。",
        "kw": "telegram两步验证,telegram二次验证,TG两步验证设置,telegram账号安全",
        "body": article1_body,
        "faqs": article1_faqs,
        "related": [
            ("telegram-account-verify-guide.html", "Telegram新账号手机号验证完整操作步骤"),
            ("telegram-login-security-tips.html", "Telegram登录安全技巧汇总"),
            ("account-verify.html", "更多账号验证教程"),
            ("index.html", "返回TG登录排查首页"),
        ],
    },
    {
        "slug": "telegram-login-security-tips",
        "title": "Telegram登录安全技巧：7招保护你的账号不被盗",
        "cat_name": "账号验证教程",
        "cat_url": "account-verify.html",
        "desc": "7个实用的Telegram登录安全技巧，从两步验遇到设备管理，帮你全面保护账号安全，防止被盗号。",
        "kw": "telegram登录安全,telegram账号保护,TG安全设置,telegram防盗号",
        "body": article2_body,
        "faqs": article2_faqs,
        "related": [
            ("telegram-two-step-verification.html", "两步验证设置教程"),
            ("telegram-login-device-management.html", "设备管理查看已登录设备"),
            ("telegram-login-fail-fix.html", "登录失败排查方法"),
            ("login-faq.html", "更多登录常见问题"),
        ],
    },
    {
        "slug": "telegram-login-device-management",
        "title": "Telegram怎么管理已登录设备？查看和退出远程设备教程",
        "cat_name": "登录常见FAQ",
        "cat_url": "login-faq.html",
        "desc": "Telegram设备管理完整教程，查看所有已登录设备、远程退出可疑设备、多设备登录注意事项。",
        "kw": "telegram设备管理,telegram查看登录设备,telegram远程退出,telegram多设备登录",
        "body": article3_body,
        "faqs": article3_faqs,
        "related": [
            ("telegram-session-logout-remote.html", "远程登出教程"),
            ("telegram-two-step-verification.html", "两步验证设置"),
            ("telegram-login-security-tips.html", "登录安全技巧"),
            ("login-faq.html", "更多登录FAQ"),
        ],
    },
    {
        "slug": "telegram-session-logout-remote",
        "title": "Telegram远程登出教程：忘退出的设备怎么远程踢下线",
        "cat_name": "登录常见FAQ",
        "cat_url": "login-faq.html",
        "desc": "Telegram远程登出完整教程，3种方法退出忘退的设备，紧急情况处理，防止账号在公共设备上被访问。",
        "kw": "telegram远程登出,telegram退出登录,telegram终止会话,telegram远程退出设备",
        "body": article4_body,
        "faqs": article4_faqs,
        "related": [
            ("telegram-login-device-management.html", "设备管理查看已登录设备"),
            ("telegram-two-step-verification.html", "两步验证设置教程"),
            ("telegram-login-security-tips.html", "登录安全技巧"),
            ("login-faq.html", "更多登录FAQ"),
        ],
    },
    {
        "slug": "telegram-login-timeout-fix",
        "title": "Telegram登录超时怎么办？5个原因和对应修复方法",
        "cat_name": "登录转圈修复",
        "cat_url": "login-spinning.html",
        "desc": "Telegram登录超时TIMEOUT错误的5个常见原因和修复方法，从网络切换到DNS修改，一步步解决。",
        "kw": "telegram登录超时,telegram TIMEOUT,telegram登录失败,telegram登录卡住",
        "body": article5_body,
        "faqs": article5_faqs,
        "related": [
            ("telegram-login-spinning-fix.html", "登录一直转圈修复方法"),
            ("telegram-login-fail-fix.html", "登录失败报错排查"),
            ("telegram-sms-code-not-received.html", "收不到验证码解决方法"),
            ("login-spinning.html", "更多登录转圈修复教程"),
        ],
    },
]

print("=== 生成新文章 ===")
for art in articles:
    html = build_article(
        art["slug"], art["title"], art["cat_name"], art["cat_url"],
        art["desc"], art["kw"], art["body"], art["faqs"], art["related"]
    )
    fpath = os.path.join(SITE_DIR, art["slug"] + ".html")
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {art['slug']}.html ({len(art['body'])} chars body)")

print(f"\n共生成 {len(articles)} 篇新文章")
