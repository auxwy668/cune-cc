// FAQ Accordion
document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.faq-q').forEach(function(q) {
    q.addEventListener('click', function() {
      var item = this.closest('.faq-item');
      var isOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item').forEach(function(i) { i.classList.remove('open'); });
      if (!isOpen) item.classList.add('open');
    });
  });

  // Platform tabs
  document.querySelectorAll('.tab-btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.tab-btn').forEach(function(b) { b.classList.remove('active'); });
      this.classList.add('active');
      var target = this.dataset.tab;
      document.querySelectorAll('.dl-tab-pane').forEach(function(p) {
        p.style.display = 'none';
      });
      var pane = document.getElementById('tab-' + target);
      if (pane) pane.style.display = 'block';
    });
  });

  // Download version selector
  document.querySelectorAll('.dl-version-item').forEach(function(item) {
    item.addEventListener('click', function() {
      document.querySelectorAll('.dl-version-item').forEach(function(i) { i.classList.remove('selected'); });
      this.classList.add('selected');
      var platform = this.dataset.platform;
      var btn = document.querySelector('.dl-main-btn');
      if (btn && platform) btn.textContent = '立即下载 ' + platform + ' 版';
    });
  });

  // TOC active state
  var tocLinks = document.querySelectorAll('.toc-list a');
  if (tocLinks.length > 0) {
    window.addEventListener('scroll', function() {
      var scrollY = window.scrollY + 100;
      tocLinks.forEach(function(link) {
        var id = link.getAttribute('href').replace('#', '');
        var el = document.getElementById(id);
        if (el) {
          if (el.offsetTop <= scrollY && el.offsetTop + el.offsetHeight > scrollY) {
            tocLinks.forEach(function(l) { l.classList.remove('active'); });
            link.classList.add('active');
          }
        }
      });
    });
  }
});


// Article TOC Generator - auto-generates TOC from H2/H3 headings
(function() {
  function generateTOC() {
    var articleBody = document.querySelector("article");
    if (!articleBody) return;
    console.log("[TOC] Found article tag:", articleBody);

    // Find all H2 and H3 headings
    var headings = articleBody.querySelectorAll("h2, h3");
    if (headings.length < 2) return; // Don't show TOC if less than 2 headings

    // Find the TOC container (try multiple IDs)
    var tocList = document.querySelector(".article-toc ul");
    if (!tocList) return;

    // Ensure all headings have IDs
    headings.forEach(function(h, idx) {
      if (!h.id) {
        h.id = "heading-" + idx;
      }
    });

    // Generate TOC items
    headings.forEach(function(h) {
      var li = document.createElement("li");
      li.className = h.tagName.toLowerCase();
      var a = document.createElement("a");
      a.href = "#" + h.id;
      a.textContent = h.textContent.replace(/^[^a-zA-Z0-9一-龥]*/, "").trim();
      li.appendChild(a);
      tocList.appendChild(li);
    });

    // Show the TOC
    document.querySelector(".article-toc").style.display = "block";
  }

  // Run on article pages
  if (document.querySelector(".article-body")) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", generateTOC);
    } else {
      generateTOC();
    }
  }
})();
