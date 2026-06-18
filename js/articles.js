// Dynamic Article Loader - Auto-generates latest articles on homepage
(function() {
  var ARTICLES_DATA = [{"file":"article1.html","title":"Telegram登录一直转圈怎么处理，手机本地设置排查步骤","category":"","excerpt":"","icon":"📄"},{"file":"article2.html","title":"TG账号登录失败常见原因与对应修复方案","category":"","excerpt":"","icon":"📄"},{"file":"article3.html","title":"Telegram收不到短信验证码，客户端自查解决办法","category":"","excerpt":"","icon":"📄"},{"file":"article4.html","title":"Telegram新账号手机号验证完整操作步骤","category":"","excerpt":"","icon":"📄"},{"file":"article5.html","title":"Telegram频繁掉线、异地登录验证常见问题汇总","category":"","excerpt":"","icon":"📄"}];

  function renderArticles() {
    var grid = document.querySelector(".articles-grid");
    if (!grid) return;

    grid.innerHTML = "";
    ARTICLES_DATA.forEach(function(art) {
      var card = document.createElement("div");
      card.className = "article-card";
      card.innerHTML = '<a href="' + art.file + '" class="article-card-link">' +
        '<div class="article-card-img"><div class="article-img-placeholder">' + art.icon + '</div></div>' +
        '<div class="article-card-body">' +
          '<div class="article-card-meta"><span class="article-category">' + art.category + '</span></div>' +
          '<h3 class="article-card-title">' + art.title + '</h3>' +
          '<p class="article-card-excerpt">' + art.excerpt + '...</p>' +
          '<div class="article-card-readmore">Read More &rarr;</div>' +
        '</div></a>';
      grid.appendChild(card);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderArticles);
  } else {
    renderArticles();
  }
})();
