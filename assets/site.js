/* icgma.github.io — 公共脚本：语言切换 / 入场动画 / 页面预加载 */
(function(){
  'use strict';

  /* ---------- 语言切换 ---------- */
  var KEY = 'icgma-lang';
  var root = document.documentElement;
  var btn = document.getElementById('langBtn');
  var titleZh = root.getAttribute('data-title-zh') || document.title;
  var titleEn = root.getAttribute('data-title-en') || document.title;

  function applyLang(l, persist){
    var isEn = (l === 'en');
    root.classList.toggle('en', isEn);
    root.lang = isEn ? 'en' : 'zh-CN';
    document.title = isEn ? titleEn : titleZh;
    if (btn){
      var label = isEn ? '切换为中文' : 'Switch to English';
      btn.title = label;
      btn.setAttribute('aria-label', label);
    }
    if (persist){
      try{ localStorage.setItem(KEY, isEn ? 'en' : 'zh'); }catch(e){}
    }
  }

  var saved = null;
  try{ saved = localStorage.getItem(KEY); }catch(e){}
  applyLang(saved === 'en' ? 'en' : 'zh', false);

  if (btn) btn.addEventListener('click', function(){
    applyLang(root.classList.contains('en') ? 'zh' : 'en', true);
  });

  /* ---------- 入场动画 ---------- */
  var els = document.querySelectorAll('.reveal');
  if (!('IntersectionObserver' in window) ||
      window.matchMedia('(prefers-reduced-motion: reduce)').matches){
    els.forEach(function(el){ el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if (e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, {threshold:.08, rootMargin:'0px 0px -6% 0px'});
    els.forEach(function(el){ io.observe(el); });
  }

  /* ---------- 页面预加载 ----------
     1) 浏览器空闲时预取导航栏其余站内页面（<link rel=prefetch as=document>）
     2) 悬停 / 聚焦 / 触摸站内页面链接时立即预取（双保险） */
  if (location.protocol === 'file:') return;

  var done = {};
  var navLinks = document.querySelectorAll('a[data-page]');

  function prefetch(href){
    if (!href || done[href]) return;
    done[href] = true;
    var l = document.createElement('link');
    l.rel = 'prefetch';
    l.href = href;
    l.as = 'document';
    document.head.appendChild(l);
  }

  function idlePreload(){
    navLinks.forEach(function(a){
      if (a.getAttribute('aria-current') !== 'page') prefetch(a.getAttribute('href'));
    });
  }
  if ('requestIdleCallback' in window) requestIdleCallback(idlePreload, {timeout:2500});
  else setTimeout(idlePreload, 1200);

  navLinks.forEach(function(a){
    var h = a.getAttribute('href');
    a.addEventListener('mouseenter', function(){ prefetch(h); }, {passive:true});
    a.addEventListener('focus', function(){ prefetch(h); }, {passive:true});
    a.addEventListener('touchstart', function(){ prefetch(h); }, {passive:true, once:true});
  });
})();
