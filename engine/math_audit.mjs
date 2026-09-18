#!/usr/bin/env node
/* ToolTide math audit: loads built pages in headless Chrome, drives the calculators
 * with known inputs, compares outputs against independently computed expectations.
 * Usage: node engine/math_audit.mjs [--base http://127.0.0.1:8980/] [--only slug,slug]
 * Exit 0 = all pass. Last line: MATH-AUDIT {json}
 */
import { spawn } from "node:child_process";
import { existsSync } from "node:fs";

const args = process.argv.slice(2);
const argOf = (n, d) => { const i = args.indexOf(n); return i >= 0 && args[i + 1] ? args[i + 1] : d; };
const BASE = argOf("--base", "http://127.0.0.1:8980/");
const only = argOf("--only", null);

const browserBin = [
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
].find(existsSync);
if (!browserBin) { console.error("no Chrome/Edge"); process.exit(1); }

const driver = (expr) => `(function(){
  const $=id=>document.getElementById(id);
  const set=(id,v)=>{const el=$(id);if(!el)return 'MISSING:'+id;el.value=v;
    el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));return null;};
  const get=id=>{const el=$(id);return el?el.textContent:'MISSING:'+id;};
  try{${expr}}catch(e){return 'ERR:'+e.message}
})()`;

const TESTS = [
  { slug: "km-to-miles", want: 6.21,
    js: `const m=set('uc-a','10'); return m||get('uc-r');` },
  { slug: "celsius-to-fahrenheit", want: 212,
    js: `const m=set('uc-a','100'); return m||get('uc-r');` },
  { slug: "kg-to-lbs", want: 110.23,
    js: `const m=set('uc-a','50'); return m||get('uc-r');` },
  { slug: "percentage-calculator", want: 30,
    js: `let m=set('p0-a','15'); if(m)return m; m=set('p0-b','200'); return m||get('p0-r');` },
  { slug: "discount-calculator", want: 40,
    js: `let m=set('dc-price','50'); if(m)return m; m=set('dc-d1','20'); return m||get('dc-final');` },
  { slug: "tip-calculator", want: 12.84,
    js: `let m=set('tip-bill','85.60'); if(m)return m; m=set('tip-split','1'); if(m)return m; m=set('tip-custom','15'); return m||get('tip-amt');` },
  { slug: "bmi-calculator", want: 22.86,
    js: `let m=set('bmi-h','175'); if(m)return m; m=set('bmi-w','70'); return m||get('bmi-out');` },
  { slug: "compound-interest-calculator", want: 1647.01, tol: 0.001,
    js: `let m=set('cp-p','1000'); if(m)return m; m=set('cp-r','5'); if(m)return m; m=set('cp-y','10'); if(m)return m; m=set('cp-m','0'); return m||get('cp-out');` },
  { slug: "loan-payment-calculator", want: 599.55, tol: 0.01,
    js: `let m=set('ln-p','20000'); if(m)return m; m=set('ln-r','5'); if(m)return m; m=set('ln-y','3'); return m||get('ln-out');` },
  { slug: "speed-distance-time", want: 2,
    js: `let m=set('sdt-d','100'); if(m)return m; m=set('sdt-s','50'); return m||get('sdt-out');` },
  { slug: "one-rep-max-calculator", want: 114, tol: 0.01,
    js: `let m=set('orm-w','100'); if(m)return m; m=set('orm-r','5'); return m||get('orm-out');` },
  { slug: "sales-tax-calculator", want: 108,
    js: `let m=set('stx-price','100'); if(m)return m; m=set('stx-rate','8'); return m||get('stx-tot');` },
  { slug: "tip-split-calculator", want: 34.5,
    js: `let m=set('ts-bill','120'); if(m)return m; m=set('ts-tip','15'); if(m)return m; m=set('ts-people','4'); return m||get('ts-out');` },
  { slug: "age-calculator", text: "36",
    js: `let m=set('age-b','1990-05-15'); if(m)return m; m=set('age-a','2026-09-19'); return m||get('age-main');` },
  { slug: "days-between-dates", want: 59,
    js: `let m=set('dd-a','2026-01-01'); if(m)return m; m=set('dd-b','2026-03-01'); return m||get('dd-days');` },
];
const tests = only ? TESTS.filter(t => only.split(",").includes(t.slug)) : TESTS;

/* ---- boot browser + CDP ---- */
const port = 9333 + Math.floor(Math.random() * 400);
const proc = spawn(browserBin, [
  `--remote-debugging-port=${port}`, "--headless=new", "--no-first-run", "--no-default-browser-check",
  "--disable-gpu", "--window-size=1280,900", "about:blank",
], { stdio: "ignore" });
const sleep = ms => new Promise(r => setTimeout(r, ms));

async function cdpConnect() {
  for (let i = 0; i < 40; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/list`);
      const tabs = await res.json();
      const page = tabs.find(t => t.type === "page");
      if (page) return new WebSocket(page.webSocketDebuggerUrl);
    } catch (e) {}
    await sleep(250);
  }
  throw new Error("no CDP");
}
const ws = await cdpConnect();
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let mid = 0; const pend = new Map();
ws.onmessage = ev => { const m = JSON.parse(ev.data); if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); } };
const send = (method, params = {}) => new Promise((res, rej) => {
  const id = ++mid; pend.set(id, m => m.error ? rej(new Error(m.error.message)) : res(m.result));
  ws.send(JSON.stringify({ id, method, params }));
  setTimeout(() => { if (pend.has(id)) { pend.delete(id); rej(new Error("cdp timeout: " + method)); } }, 20000);
});

const results = [];
for (const t of tests) {
  const url = BASE.replace(/\/?$/, "/") + t.slug + "/";
  try {
    await send("Page.navigate", { url });
    await sleep(700);
    const r = await send("Runtime.evaluate", { expression: driver(t.js), returnByValue: true });
    const raw = String(r.result?.value ?? "NO-VALUE");
    if (/^(MISSING|ERR)/.test(raw)) {
      results.push({ slug: t.slug, ok: false, why: raw, raw });
    } else if (t.text) {
      const ok = raw.includes(t.text);
      results.push({ slug: t.slug, ok, why: ok ? "" : `expected text "${t.text}"`, raw });
    } else {
      const num = parseFloat(String(raw).replace(/[^\d.,-]/g, "").replace(/,/g, "").match(/-?\d+(\.\d+)?/)?.[0]);
      const tol = t.tol ?? 0.005;
      const ok = isFinite(num) && Math.abs(num - t.want) <= Math.abs(t.want) * tol + 1e-9;
      results.push({ slug: t.slug, ok, why: ok ? "" : `got ${num}, want ${t.want}`, raw });
    }
  } catch (e) {
    results.push({ slug: t.slug, ok: false, why: "nav/eval: " + e.message });
  }
  console.log(`${results.at(-1).ok ? "PASS" : "FAIL"}  ${t.slug}  ${results.at(-1).why || ""} [${results.at(-1).raw || ""}]`);
}
proc.kill();
const fails = results.filter(r => !r.ok);
console.log("MATH-AUDIT " + JSON.stringify({ total: results.length, failed: fails.length,
  fails: fails.map(f => ({ slug: f.slug, why: f.why })) }));
process.exit(fails.length ? 1 : 0);
