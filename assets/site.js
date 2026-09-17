/* icgma.github.io — 公共脚本：语言切换 / 入场动画 / 页面预加载 */
(function(){
  'use strict';

  /* ---------- 语言切换 ---------- */
  var KEY = 'icgma-lang';
  var btn = document.getElementById('langBtn');
  var titleZh = document.documentElement.getAttribute('data-title-zh') || document.title;
  var titleEn = document.documentElement.getAttribute('data-title-en') || document.title;

  function setLang(l){
    document.body.classList.toggle('en', l === 'en');
    document.body.classList.toggle('zh', l !== 'en');
    document.documentElement.lang = (l === 'en') ? 'en' : 'zh-CN';
    document.title = (l === 'en') ? titleEn : titleZh;
    if (btn) btn.textContent = (l === 'en') ? '中文' : 'EN';
    try{ localStorage.setItem(KEY, l); }catch(e){}
  }

  var saved = null;
  try{ saved = localStorage.getItem(KEY); }catch(e){}
  if (saved === 'en') setLang('en');
  if (btn) btn.addEventListener('click', function(){
    setLang(document.body.classList.contains('en') ? 'zh' : 'en');
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
     1) 浏览器空闲时预取本站其余页面（<link rel=prefetch as=document>）
     2) 悬停 / 聚焦站内页面链接时立即预取（双保险） */
  var PAGES = ['index.html','courses.html','software.html','working.html','resources.html'];
  var done = {};

  function prefetch(href){
    if (done[href]) return;
    done[href] = true;
    var l = document.createElement('link');
    l.rel = 'prefetch';
    l.href = href;
    l.as = 'document';
    document.head.appendChild(l);
  }

  function idlePreload(){
    var here = location.pathname.split('/').pop() || 'index.html';
    PAGES.forEach(function(p){ if (p !== here) prefetch(p); });
  }
  if ('requestIdleCallback' in window) requestIdleCallback(idlePreload, {timeout:2500});
  else setTimeout(idlePreload, 1200);

  document.querySelectorAll('a[data-page]').forEach(function(a){
    var h = a.getAttribute('href');
    a.addEventListener('mouseenter', function(){ prefetch(h); }, {passive:true});
    a.addEventListener('focus', function(){ prefetch(h); }, {passive:true});
    a.addEventListener('touchstart', function(){ prefetch(h); }, {passive:true, once:true});
  });
})();
