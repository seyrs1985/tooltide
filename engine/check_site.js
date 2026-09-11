// Syntax-check all inline scripts + JSON-LD in the built site.
const fs = require('fs'), path = require('path'), vm = require('vm');
const root = path.join(__dirname, '..', 'docs');
let files = [];
(function walk(d) {
  for (const f of fs.readdirSync(d)) {
    const p = path.join(d, f);
    if (fs.statSync(p).isDirectory()) walk(p);
    else if ((f === 'index.html' || f === '404.html') && !p.includes(`${path.sep}play${path.sep}`)) files.push(p);
  }
})(root);
let fail = 0, checked = 0;
for (const f of files) {
  const html = fs.readFileSync(f, 'utf8');
  const scripts = [...html.matchAll(/<script(?![^>]*ld\+json)[^>]*>([\s\S]*?)<\/script>/g)];
  for (const [i, s] of scripts.entries()) {
    if (!s[1].trim()) continue;
    try { new vm.Script(s[1], { filename: f + '#' + i }); checked++; }
    catch (e) { fail++; console.log('JS FAIL', f, i, e.message); }
  }
  const lds = [...html.matchAll(/<script[^>]*ld\+json[^>]*>([\s\S]*?)<\/script>/g)];
  for (const l of lds) {
    try { JSON.parse(l[1]); checked++; }
    catch (e) { fail++; console.log('LD FAIL', f, e.message); }
  }
  if (!/canonical/.test(html)) { fail++; console.log('NO CANONICAL', f); }
}
// site-level assertions: back-to-top, 3-level breadcrumbs, category counts
try {
  const assert = (cond, msg) => { checked++; if (!cond) { fail++; console.log('SITE FAIL', msg); } };
  const idx = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
  assert(idx.includes('id="to-top"'), 'homepage: back-to-top button');
  assert((idx.match(/class="cat-count"/g) || []).length >= 5, 'homepage: cat-count badges (>=5)');
  assert((idx.match(/chip-n/g) || []).length >= 5, 'homepage: chip counts (>=5)');
  const tool = fs.readFileSync(path.join(root, 'celsius-to-fahrenheit', 'index.html'), 'utf8');
  const crumbNav = tool.match(/<nav class="crumbs[\s\S]*?<\/nav>/);
  assert(!!crumbNav && crumbNav[0].includes('#converter'), 'tool page: crumb links category anchor');
  // header search: every non-home page GETs the homepage ?q= contract
  const hsForm = tool.match(/<form class="head-search"[^>]*>/);
  const canon = (tool.match(/<link rel="canonical" href="([^"]+)"/) || [])[1] || '';
  const hsBase = canon.replace(/celsius-to-fahrenheit\/$/, '');
  assert(!!hsForm && hsForm[0].includes('action="' + hsBase + '"') && hsForm[0].includes('method="get"')
    && /<input[^>]*name="q"/.test(tool), 'tool page: header search form GETs site base with q param');
  const graph = [...tool.matchAll(/<script[^>]*ld\+json[^>]*>([\s\S]*?)<\/script>/g)]
    .map(m => JSON.parse(m[1])).flatMap(j => j['@graph'] || []);
  const bc = graph.find(n => n['@type'] === 'BreadcrumbList');
  assert(!!bc && bc.itemListElement.length === 3
    && bc.itemListElement[1].name === 'Converters'
    && bc.itemListElement.map(x => x.position).join(',') === '1,2,3',
    'tool page: BreadcrumbList has 3 ordered levels');
  const css = fs.readFileSync(path.join(root, 'style.css'), 'utf8');
  assert(/\.to-top\b/.test(css) && /\.cat-count\b/.test(css) && /\.chip-n\b/.test(css),
    'style.css: to-top/cat-count/chip-n rules');
  assert(/\.faq summary::after/.test(css) && /\.faq\[open\] summary::after/.test(css),
    'style.css: faq disclosure marker');
  assert(/scroll-margin-top/.test(css), 'style.css: anchor scroll-margin');
  assert(/::selection/.test(css), 'style.css: selection tint');
  assert(/noscript-note/.test(css), 'style.css: noscript notice style');
  assert(tool.includes('<noscript') && tool.includes('noscript-note'),
    'tool page: noscript JS-required notice');

  // homepage ?q= deep-link search must actually run (SearchAction contract)
  const searchScript = [...idx.matchAll(/<script(?![^>]*ld\+json)[^>]*>([\s\S]*?)<\/script>/g)]
    .map(m => m[1]).find(s => s.includes('var CARDS='));
  if (searchScript) {
    try {
      const listeners = {};
      const inp = { value: '', addEventListener: (t, f) => { listeners[t] = f; },
        dispatchEvent: ev => { listeners[ev.type].call(inp, ev); } };
      const out = { style: {}, innerHTML: '' };
      const live = { textContent: '' };
      const sb = {
        document: {
          getElementById: id => (id === 'tool-search' ? inp : id === 'search-results' ? out
            : id === 'search-status' ? live : null),
          querySelectorAll: () => [],
          addEventListener: (t, f) => { listeners['doc:' + t] = f; },
          activeElement: { tagName: '' }
        },
        location: { search: '' },
        URLSearchParams, Event: class { constructor(t) { this.type = t; } },
        console
      };
      vm.createContext(sb);
      const run = search => {
        inp.value = ''; out.innerHTML = ''; out.style.display = '';
        sb.location = { search };
        new vm.Script(searchScript, { filename: 'index.html#search' }).runInContext(sb);
      };
      assert(searchScript.includes('URLSearchParams(location.search)'),
        'homepage: search script reads ?q= param');
      run('?q=f%20to%20c');
      assert(inp.value === 'f to c' && out.style.display === 'grid'
        && /Fahrenheit/i.test(out.innerHTML), 'homepage: ?q=f to c deep-link renders results');
      assert(/match/i.test(live.textContent) && live.textContent.includes('f to c'),
        'homepage: search status announces the match count');
      inp.value = '';
      inp.dispatchEvent({ type: 'input' });
      assert(live.textContent === '', 'homepage: clearing the query clears the status line');
      run('?q=zzqqxx');
      assert(/No tools match/.test(out.innerHTML), 'homepage: ?q= empty state message');
    } catch (e) { fail++; console.log('SITE FAIL search deep-link:', e.message); }
  } else { fail++; console.log('SITE FAIL homepage: search script not found'); }

  // header search hidden where a search box is already on screen
  assert(idx.includes('body class="home"') && /body\.home \.head-search\{display:none\}/.test(css)
    && /body\.fourohfour \.head-search\{display:none\}/.test(css),
    'header search hidden on homepage/404 (duplicate search box)');
  // OpenSearch autodiscovery + description file reusing the ?q= contract
  assert(/rel="search"[^>]*opensearchdescription/.test(idx), 'homepage: OpenSearch autodiscovery link');
  const osd = fs.readFileSync(path.join(root, 'opensearch.xml'), 'utf8');
  assert(/<OpenSearchDescription/.test(osd) && osd.includes('?q={searchTerms}'),
    'opensearch.xml: search template hits the ?q= contract');

  // manual theme toggle: CSS coverage + markup + stub-DOM behavior of THEME_JS
  assert(/html\[data-theme="dark"\]\{[^}]*--bg:#0f172a/.test(css.replace(/\n/g, '')),
    'style.css: explicit dark palette block (data-theme="dark")');
  assert(/@media\(prefers-color-scheme:dark\)\{\s*html:not\(\[data-theme="light"\]\)\{/.test(css),
    'style.css: OS dark fallback excludes explicit light choice');
  assert(/html\.js \.theme-toggle\{display:inline-flex\}/.test(css) && /\.theme-toggle\{display:none/.test(css),
    'style.css: theme toggle hidden without JS, visible with JS');
  assert(idx.includes('id="theme-toggle"') && /tt-theme/.test(idx),
    'homepage: theme toggle button + pre-paint restore script');
  const themeScript = [...idx.matchAll(/<script(?![^>]*ld\+json)[^>]*>([\s\S]*?)<\/script>/g)]
    .map(m => m[1]).find(s => s.includes("getElementById('theme-toggle')"));
  if (themeScript) {
    const makeSandbox = (stored, osDark) => {
      const saved = { v: stored || null };
      const htmlEl = { attrs: {}, getAttribute: k => htmlEl.attrs[k] || null, setAttribute: (k, v) => { htmlEl.attrs[k] = v; } };
      const icon = { textContent: '' };
      const btn = { label: '', handlers: {}, icon,
        querySelector: () => icon,
        setAttribute: (k, v) => { if (k === 'aria-label') btn.label = v; },
        addEventListener: (t, f) => { btn.handlers[t] = f; } };
      const metas = [{ media: 'x', content: '', removeAttribute() { this.media = null; }, setAttribute(k, v) { this[k] = v; } },
                     { media: 'y', content: '', removeAttribute() { this.media = null; }, setAttribute(k, v) { this[k] = v; } }];
      const sb = {
        document: {
          documentElement: htmlEl,
          getElementById: id => (id === 'theme-toggle' ? btn : null),
          querySelectorAll: () => metas
        },
        window: { matchMedia: q => ({ matches: osDark && /dark/.test(q) }) },
        localStorage: { getItem: () => saved.v, setItem: (k, v) => { saved.v = v; } }
      };
      vm.createContext(sb);
      new vm.Script(themeScript, { filename: 'index.html#theme' }).runInContext(sb);
      return { htmlEl, btn, metas, saved, click: () => btn.handlers.click() };
    };
    try {
      const s1 = makeSandbox(null, false);
      assert(s1.htmlEl.attrs['data-theme'] === 'light' && /dark/i.test(s1.btn.label),
        'theme: initial paint follows OS light, label offers dark');
      s1.click();
      assert(s1.htmlEl.attrs['data-theme'] === 'dark' && s1.saved.v === 'dark'
        && s1.metas.every(m => m.media === null && m.content === '#1e293b')
        && /light/i.test(s1.btn.label),
        'theme: click flips to dark, saves tt-theme, syncs theme-color metas');
      const s2 = makeSandbox('dark', false);
      assert(s2.htmlEl.attrs['data-theme'] === 'dark',
        'theme: saved preference reapplied on next visit (OS light)');
      const s3 = makeSandbox('light', true);
      assert(s3.htmlEl.attrs['data-theme'] === 'light',
        'theme: explicit light wins over OS dark');
    } catch (e) { fail++; console.log('SITE FAIL theme toggle stub:', e.message); }
  } else { fail++; console.log('SITE FAIL homepage: theme toggle script not found'); }

  // 404 page: dedicated search form feeding the homepage ?q= contract
  const p404 = fs.readFileSync(path.join(root, '404.html'), 'utf8');
  assert(/<form class="four04-search"[^>]*action="[^"]*"[^>]*method="get"[^>]*>\s*<input[^>]*name="q"/.test(p404.replace(/\n/g, ' ')),
    '404 page: GET search form with q param');
  assert(p404.includes('body class="fourohfour"'), '404 page: body class for header-search hide');
  const priv = fs.readFileSync(path.join(root, 'privacy', 'index.html'), 'utf8');
  assert(/theme choice, saved via local storage/.test(priv),
    'privacy page: theme localStorage disclosure matches behavior');
} catch (e) { fail++; console.log('SITE FAIL round-assertions:', e.message); }

console.log('files:', files.length, '| checks passed:', checked, '| failures:', fail);
if (fail > 0) process.exit(1);
