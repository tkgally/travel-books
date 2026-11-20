// Display settings for every page of the site: colours, size of text, typeface, spacing, column width, underlined
// links; and for the text of a book justification, paragraph style, correction marks, page numbers, the reader's place. The choices are kept in this browser (localStorage) and
// nowhere else. The site works without this file: the "Display" button is made here, so that a reader whose
// browser does not run scripts sees no control that does nothing. Styles: site.css, "Display settings".
(function () {
  'use strict';
  var KEY = 'tb-display', PLACES = 'tb-place', KEEP = 100;
  var root = document.documentElement;
  var DEF = { theme: 'auto', font: 'serif', align: 'justify', para: 'indent', size: 1, lh: 1.6, width: 36, ls: 0, ws: 0,
              corr: 1, links: 1, pb: 0, place: 1 };
  var CHOICES = { theme: ['auto', 'light', 'sepia', 'dark'], font: ['serif', 'sans', 'default'],
                  align: ['justify', 'left'], para: ['indent', 'block'] };
  var STEPS = { size: [0.8, 0.9, 1, 1.1, 1.25, 1.4, 1.6, 1.8, 2], lh: [1.3, 1.45, 1.6, 1.8, 2, 2.3],
                width: [24, 30, 36, 44, 54, 66], ls: [0, 0.03, 0.06, 0.09, 0.12], ws: [0, 0.08, 0.16, 0.24, 0.32] };
  var UNIT = { size: '', lh: '', width: 'rem', ls: 'em', ws: 'em' };
  var FLAGS = ['corr', 'links', 'pb', 'place'];
  var s = load();

  function get(key) { try { return localStorage.getItem(key); } catch (e) { return null; } }
  function put(key, value) { try { localStorage.setItem(key, value); } catch (e) {} }

  // Only values from the lists above are accepted: what is stored ends up in the page's styles.
  function load() {
    var raw = {}, out = {}, k;
    try { raw = JSON.parse(get(KEY)) || {}; } catch (e) { raw = {}; }
    for (k in DEF) out[k] = DEF[k];
    for (k in CHOICES) if (CHOICES[k].indexOf(raw[k]) >= 0) out[k] = raw[k];
    for (k in STEPS) if (STEPS[k].indexOf(raw[k]) >= 0) out[k] = raw[k];
    FLAGS.forEach(function (f) { if (raw[f] === 0 || raw[f] === 1) out[f] = raw[f]; });
    if (!('pb' in raw) && get('showpb') === '1') out.pb = 1;     // the choice made before these settings existed
    return out;
  }

  function save() {
    var out = {}, k;
    for (k in DEF) if (s[k] !== DEF[k]) out[k] = s[k];
    put(KEY, JSON.stringify(out));
  }

  function attr(name, value) { if (value) root.setAttribute(name, value); else root.removeAttribute(name); }

  function apply() {
    var k;
    attr('data-theme', s.theme === 'auto' ? '' : s.theme);
    attr('data-font', s.font === DEF.font ? '' : s.font);
    attr('data-align', s.align === DEF.align ? '' : s.align);
    attr('data-para', s.para === DEF.para ? '' : s.para);
    attr('data-corr', s.corr ? '' : 'off');
    attr('data-links', s.links ? '' : 'off');
    for (k in STEPS) {
      if (s[k] === DEF[k]) root.style.removeProperty('--tb-' + k);
      else root.style.setProperty('--tb-' + k, s[k] + UNIT[k]);
    }
    root.classList.toggle('showpb', !!s.pb || location.hash.indexOf('#pg-') === 0);
  }

  root.classList.add('tb-js');
  apply();                       // before the page is drawn: this file is loaded in the head, without "defer"

  // ---- the reader's place: the chapter and the paragraph last read, for each book ----

  var where = location.pathname.match(/\/books\/([^\/]+)\/([^\/]*)$/);
  var bookId = where && where[1], file = where && (where[2] || 'index.html');

  function places() {
    var p;
    try { p = JSON.parse(get(PLACES)); } catch (e) {}
    return p && typeof p === 'object' ? p : {};
  }

  function savePlace(article) {
    var kids = article.children, i, p, ids;
    for (i = 0; i < kids.length; i++) if (kids[i].getBoundingClientRect().bottom > 0) break;
    p = places();
    p[bookId] = { f: file, b: i, t: Date.now() };
    ids = Object.keys(p);
    if (ids.length > KEEP) {
      ids.sort(function (a, b) { return (p[a].t || 0) - (p[b].t || 0); });
      ids.slice(0, ids.length - KEEP).forEach(function (id) { delete p[id]; });
    }
    put(PLACES, JSON.stringify(p));
  }

  function chapterPlace(article) {
    var p = places()[bookId], nav = performance.getEntriesByType && performance.getEntriesByType('navigation')[0];
    var touched = false, timer = 0;
    function go() {
      var el = article.children[p.b];
      if (el && !touched) el.scrollIntoView();
    }
    // Back, forward and reload are left to the browser, which returns to the place itself.
    if (s.place && p && p.f === file && p.b > 0 && !location.hash && (!nav || nav.type === 'navigate')) {
      ['wheel', 'touchstart', 'keydown', 'mousedown'].forEach(function (ev) {
        window.addEventListener(ev, function () { touched = true; }, { passive: true, once: true });
      });
      go();
      window.addEventListener('load', go);      // again when the pictures above have taken their room
    }
    window.addEventListener('scroll', function () {
      if (!s.place || timer) return;
      timer = setTimeout(function () { timer = 0; if (s.place) savePlace(article); }, 400);
    }, { passive: true });
  }

  function resumeLink() {
    var p = places()[bookId], h = document.getElementById('contents'), old = document.querySelector('.tb-resume'), a, para, t;
    if (old) old.parentNode.removeChild(old);
    if (!s.place || !p || !h || !/^\d+\.html$/.test(p.f)) return;
    a = document.createElement('a');
    a.href = p.f;
    t = document.querySelector('nav.toc a[href="' + p.f + '"]');
    a.textContent = 'Continue reading' + (t ? ': ' + t.textContent : '');
    para = document.createElement('p');
    para.className = 'tb-resume';
    para.appendChild(a);
    h.parentNode.insertBefore(para, h);
  }

  // ---- the "Display" button and its panel (every page) ----

  var LINES = { tight: 'M4 8h16M4 12h16M4 16h16', loose: 'M4 5h16M4 12h16M4 19h16',
    narrow: 'M10 5v14M14 5v14M2 12h5M5 10l2 2-2 2M22 12h-5M19 10l-2 2 2 2',
    wide: 'M3 5v14M21 5v14M11 12H6M8 10l-2 2 2 2M13 12h5M16 10l2 2-2 2',
    justify: 'M3 6h18M3 10h18M3 14h18M3 18h18', left: 'M3 6h18M3 10h12M3 14h16M3 18h9',
    indent: 'M8 4h13M3 8h18M3 12h11M8 16h13M3 20h18', block: 'M3 4h18M3 8h11M3 15h18M3 19h11',
    place: 'M7 3h10v18l-5-4-5 4z', reset: 'M4 12a8 8 0 1 0 2.6-5.9M4 4v5h5',
    more: 'M5 9l7 7 7-7' };
  function svg(name) { return '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="' + LINES[name] + '"/></svg>'; }
  function txt(cls, text, style) {
    return '<span aria-hidden="true" class="' + cls + '"' + (style ? ' style="' + style + '"' : '') + '>' + text + '</span>';
  }
  var ui = null;      // { refresh: function } once the panel exists

  function el(tag, props, html) {
    var e = document.createElement(tag), k;
    for (k in props) e.setAttribute(k, props[k]);
    if (html) e.innerHTML = html;
    return e;
  }

  function buildUI(article) {
    var header = document.querySelector('header.site'), list = header && header.querySelector('nav ul');
    if (!list) return;
    var refreshers = [];
    var li = el('li'), btn = el('button', { type: 'button', 'class': 'tb-btn', 'aria-expanded': 'false', 'aria-controls': 'tb-panel' });
    btn.textContent = 'Display';
    li.appendChild(btn);
    list.appendChild(li);
    var panel = el('div', { id: 'tb-panel', 'class': 'tb-panel', role: 'group', 'aria-label': 'Display settings', hidden: '' });
    var adv = el('div', { id: 'tb-adv', 'class': 'tb-adv', hidden: '' });
    var status = el('span', { 'class': 'tb-sr', role: 'status' });
    var tip = el('div', { 'class': 'tb-tip', 'aria-hidden': 'true', hidden: '' });

    function changed() { apply(); save(); refresh(); }
    function refresh() { refreshers.forEach(function (f) { f(); }); }

    function choice(parent, key, label, options) {       // options: [value, name, picture]
      var row = el('div', { 'class': 'tb-row', role: 'radiogroup', 'aria-label': label });
      options.forEach(function (o) {
        var lab = el('label', { 'class': 'tb-opt', 'data-tip': o[1] });
        var input = el('input', { type: 'radio', name: 'tb-' + key, value: o[0], 'aria-label': o[1] });
        input.addEventListener('change', function () { s[key] = o[0]; changed(); });
        refreshers.push(function () { input.checked = s[key] === o[0]; });
        lab.appendChild(input);
        lab.insertAdjacentHTML('beforeend', o[2].indexOf('<svg') === 0 ? '<span>' + o[2] + '</span>' : o[2]);
        row.appendChild(lab);
      });
      parent.appendChild(row);
    }

    function stepper(parent, key, label, less, more, say) {       // less, more: [name, picture]
      var row = el('div', { 'class': 'tb-row', role: 'group', 'aria-label': label });
      var steps = STEPS[key], dots = el('span', { 'class': 'tb-dots', 'aria-hidden': 'true' });
      var down = el('button', { type: 'button', 'aria-label': less[0], 'data-tip': less[0] }, less[1]);
      var up = el('button', { type: 'button', 'aria-label': more[0], 'data-tip': more[0] }, more[1]);
      steps.forEach(function () { dots.appendChild(el('i')); });
      function move(by) {
        var i = steps.indexOf(s[key]) + by;
        if (i < 0 || i >= steps.length) return;
        s[key] = steps[i];
        changed();
        status.textContent = label + ': ' + (say ? say(s[key]) : (i + 1) + ' of ' + steps.length);
        if (down.disabled) up.focus(); else if (up.disabled) down.focus();     // the end of the scale: keep the keyboard's place
      }
      down.addEventListener('click', function () { move(-1); });
      up.addEventListener('click', function () { move(1); });
      refreshers.push(function () {
        var i = steps.indexOf(s[key]), k;
        down.disabled = i <= 0;
        up.disabled = i >= steps.length - 1;
        for (k = 0; k < steps.length; k++) dots.children[k].className = k === i ? 'on' : '';
      });
      row.appendChild(down); row.appendChild(dots); row.appendChild(up);
      parent.appendChild(row);
    }

    function toggle(row, key, label, picture, after) {
      var b = el('button', { type: 'button', 'aria-label': label, 'data-tip': label }, picture);
      b.addEventListener('click', function () { s[key] = s[key] ? 0 : 1; changed(); if (after) after(); });
      refreshers.push(function () { b.setAttribute('aria-pressed', s[key] ? 'true' : 'false'); });
      row.appendChild(b);
    }

    // basic
    choice(panel, 'theme', 'Colours', [
      ['auto', 'Colours: as this device is set', txt('tb-sw tb-sw-auto', '')],
      ['light', 'Colours: light', txt('tb-sw tb-sw-light', 'A')],
      ['sepia', 'Colours: sepia', txt('tb-sw tb-sw-sepia', 'A')],
      ['dark', 'Colours: dark', txt('tb-sw tb-sw-dark', 'A')]]);
    stepper(panel, 'size', 'Size of the text', ['Smaller text', txt('tb-a-small', 'A')], ['Larger text', txt('tb-a-large', 'A')],
            function (v) { return Math.round(v * 100) + '%'; });
    choice(panel, 'font', 'Typeface', [
      ['serif', 'Typeface: serif', txt('tb-f-serif', 'Aa')],
      ['sans', 'Typeface: sans serif', txt('tb-f-sans', 'Aa')],
      ['default', 'Typeface: the one set in this browser', txt('tb-f-default', 'Aa')]]);
    stepper(panel, 'lh', 'Space between lines', ['Lines closer together', svg('tight')], ['Lines further apart', svg('loose')]);
    var moreRow = el('div', { 'class': 'tb-row' });
    var more = el('button', { type: 'button', 'aria-expanded': 'false', 'aria-controls': 'tb-adv', 'aria-label': 'More settings',
                              'data-tip': 'More settings' }, svg('more'));
    more.addEventListener('click', function () {
      adv.hidden = !adv.hidden;
      more.setAttribute('aria-expanded', adv.hidden ? 'false' : 'true');
      more.firstChild.style.transform = adv.hidden ? '' : 'rotate(180deg)';
    });
    moreRow.appendChild(more);
    panel.appendChild(moreRow);

    // advanced
    stepper(adv, 'width', 'Width of the column', ['Narrower column', svg('narrow')], ['Wider column', svg('wide')]);
    var pair = el('div', { 'class': 'tb-row tb-wrap' });
    adv.appendChild(pair);
    choice(pair, 'align', 'Right-hand edge', [
      ['justify', 'Even right-hand edge (justified)', svg('justify')],
      ['left', 'Ragged right-hand edge, no hyphenation', svg('left')]]);
    choice(pair, 'para', 'Paragraphs', [
      ['indent', 'Paragraphs: first line indented', svg('indent')],
      ['block', 'Paragraphs: a space between them', svg('block')]]);
    stepper(adv, 'ls', 'Space between letters', ['Letters closer together', txt('', 'abc', 'letter-spacing:-0.03em')],
            ['Letters further apart', txt('', 'abc', 'letter-spacing:0.25em;margin-right:-0.25em')]);
    stepper(adv, 'ws', 'Space between words', ['Words closer together', txt('', 'ab cd')],
            ['Words further apart', txt('', 'ab cd', 'word-spacing:0.5em')]);
    var flags = el('div', { 'class': 'tb-row', role: 'group', 'aria-label': 'Shown or not' });
    toggle(flags, 'links', 'Underline links (all pages)', txt('tb-i-link', 'abc'));
    toggle(flags, 'corr', 'Mark corrected misprints with dots', txt('tb-i-corr', 'abc'));
    toggle(flags, 'pb', 'Show the page numbers of the printed book (each links to the scanned page)', txt('tb-i-pb', '12'));
    toggle(flags, 'place', 'Remember my place in each book', svg('place'), function () {
      if (s.place) { if (article && bookId) savePlace(article); } else try { localStorage.removeItem(PLACES); } catch (e) {}
    });
    adv.appendChild(flags);
    var resetRow = el('div', { 'class': 'tb-row' });
    var reset = el('button', { type: 'button', 'aria-label': 'Back to the settings the site starts with',
                               'data-tip': 'Back to the settings the site starts with' }, svg('reset'));
    reset.addEventListener('click', function () {
      for (var k in DEF) s[k] = DEF[k];
      changed();
      status.textContent = 'The settings are as the site starts with.';
    });
    resetRow.appendChild(reset);
    adv.appendChild(resetRow);
    panel.appendChild(adv);
    panel.appendChild(status);
    panel.appendChild(tip);

    header.appendChild(panel);
    var old = document.querySelector('.pbtoggle');     // the checkbox for readers without the script
    if (old) old.parentNode.removeChild(old);
    refresh();

    function open(yes) {
      panel.hidden = !yes;
      btn.setAttribute('aria-expanded', yes ? 'true' : 'false');
      tip.hidden = true;
    }
    btn.addEventListener('click', function () { open(panel.hidden); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !panel.hidden) { open(false); btn.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (!panel.hidden && !panel.contains(e.target) && !btn.contains(e.target)) open(false);
    });

    // The names of the controls, shown beside them for a mouse or a keyboard (a touch screen has no hovering).
    function showTip(target) {
      var t = target && target.closest && target.closest('[data-tip]'), r, p, left;
      if (!t || !panel.contains(t)) { tip.hidden = true; return; }
      tip.textContent = t.getAttribute('data-tip');
      tip.style.whiteSpace = 'nowrap';
      tip.hidden = false;
      r = t.getBoundingClientRect(); p = panel.getBoundingClientRect();
      if (tip.offsetWidth > p.width - 8) tip.style.whiteSpace = 'normal';
      left = r.left - p.left + r.width / 2 - tip.offsetWidth / 2;
      left = Math.max(4, Math.min(left, p.width - tip.offsetWidth - 6));
      tip.style.left = left + 'px';
      tip.style.top = (r.bottom - p.top + 4) + 'px';
    }
    if (window.matchMedia && matchMedia('(hover: hover)').matches) {
      panel.addEventListener('mouseover', function (e) { showTip(e.target); });
      panel.addEventListener('mouseleave', function () { tip.hidden = true; });
    }
    panel.addEventListener('focusin', function (e) {
      var keyboard = false;
      try { keyboard = e.target.matches(':focus-visible'); } catch (x) {}
      if (keyboard) showTip(e.target); else tip.hidden = true;
    });
    panel.addEventListener('focusout', function () { tip.hidden = true; });

    ui = { refresh: refresh };
  }

  function ready() {
    var article = document.querySelector('article.book');
    buildUI(article);
    if (article) { if (bookId) chapterPlace(article); }
    else if (bookId && file === 'index.html') resumeLink();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready); else ready();

  // A change made in another tab or window reaches this one.
  window.addEventListener('storage', function (e) {
    if (e.key !== KEY && e.key !== null) return;
    s = load(); apply();
    if (ui) ui.refresh();
  });
  // A page brought back by the Back button is shown as it was left: bring it up to date.
  window.addEventListener('pageshow', function (e) {
    if (!e.persisted) return;
    s = load(); apply();
    if (ui) ui.refresh();
    if (bookId && file === 'index.html' && !document.querySelector('article.book')) resumeLink();
  });
})();
