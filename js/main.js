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
