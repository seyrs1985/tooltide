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
      const sb = {
        document: {
          getElementById: id => (id === 'tool-search' ? inp : id === 'search-results' ? out : null),
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
      run('?q=zzqqxx');
      assert(/No tools match/.test(out.innerHTML), 'homepage: ?q= empty state message');
    } catch (e) { fail++; console.log('SITE FAIL search deep-link:', e.message); }
  } else { fail++; console.log('SITE FAIL homepage: search script not found'); }
} catch (e) { fail++; console.log('SITE FAIL round-assertions:', e.message); }

console.log('files:', files.length, '| checks passed:', checked, '| failures:', fail);
if (fail > 0) process.exit(1);
