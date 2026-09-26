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

/* TESTS + verify moved to qa_expectations.mjs (shared with qa_patrol --strict) */
import { TESTS } from "./qa_expectations.mjs";
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
    } else if (t.cons) {
      // macros consistency: grams split must sum back to the calorie input (4/4/9 kcal per g)
      const [pg, cg, fg] = raw.split("|").map(s => parseFloat(String(s).replace(/[^\d.]/g, "")));
      const sum = (pg || 0) * 4 + (cg || 0) * 4 + (fg || 0) * 9;
      const ok = isFinite(sum) && Math.abs(sum - t.cons) <= t.cons * 0.01;
      results.push({ slug: t.slug, ok, why: ok ? "" : `grams sum to ${sum}, want ${t.cons}`, raw });
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
