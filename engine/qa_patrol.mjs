#!/usr/bin/env node
/* ToolDune page patrol: loads LIVE pages in headless Chrome, checks console errors,
 * does a generic interact probe (first input -> fill -> no error), DOM health.
 * Usage: node engine/qa_patrol.mjs --slugs a,b,c [--base https://tooldune.com/]
 * Exit 0 = all clean. Last line: PAGE-PATROL {json}
 */
import { spawn } from "node:child_process";
import { existsSync, appendFileSync } from "node:fs";
import { TESTS as EXPECTS, verify } from "./qa_expectations.mjs";

const args = process.argv.slice(2);
const argOf = (n, d) => { const i = args.indexOf(n); return i >= 0 && args[i + 1] ? args[i + 1] : d; };
const BASE = argOf("--base", "https://tooldune.com/");
const slugs = (argOf("--slugs", "") || "").split(",").map(s => s.trim()).filter(Boolean);
const strictAll = args.includes("--strict"); // run expectation asserts whenever batch hits a known rule
if (!slugs.length) { console.error("no slugs"); process.exit(2); }

const STRICT_DRV = (expr) => `(function(){
  const $=id=>document.getElementById(id);
  const set=(id,v)=>{const el=$(id);if(!el)return 'MISSING:'+id;el.value=v;
    el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));return null;};
  const get=id=>{const el=$(id);return el?el.textContent:'MISSING:'+id;};
  try{${expr}}catch(e){return 'ERR:'+e.message}
})()`;

const browserBin = [
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
  "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
].find(existsSync);
if (!browserBin) { console.error("no Chrome/Edge"); process.exit(1); }

const port = 9733 + Math.floor(Math.random() * 400);
const proc = spawn(browserBin, [
  `--remote-debugging-port=${port}`, "--headless=new", "--no-first-run", "--no-default-browser-check",
  "--disable-gpu", "--window-size=390,844", "about:blank",
], { stdio: "ignore" }); // mobile-ish viewport 390x844
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
const consoleErrs = [];
ws.onmessage = ev => {
  const m = JSON.parse(ev.data);
  if (m.id && pend.has(m.id)) { pend.get(m.id)(m); pend.delete(m.id); return; }
  if (m.method === "Runtime.consoleAPICalled" && ["error", "assert"].includes(m.params?.type))
    consoleErrs.push(m.params.args.map(a => a.value ?? a.description ?? "").join(" ").slice(0, 300));
  if (m.method === "Runtime.exceptionThrown")
    consoleErrs.push(String(m.params?.exceptionDetails?.exception?.description || m.params?.exceptionDetails?.text || "exception").slice(0, 300));
};
const send = (method, params = {}) => new Promise((res, rej) => {
  const id = ++mid; pend.set(id, m => m.error ? rej(new Error(m.error.message)) : res(m.result));
  ws.send(JSON.stringify({ id, method, params }));
  setTimeout(() => { if (pend.has(id)) { pend.delete(id); rej(new Error("cdp timeout: " + method)); } }, 20000);
});

async function httpStatus(url) {
  try { const r = await fetch(url); return r.status; } catch (e) { return "ERR:" + e.message.slice(0, 80); }
}

const PROBE = `(function(){
  const out = {title: document.title || "", overflow: false, hasInput: false, interacted: false, btnOk: false};
  const de = document.documentElement;
  out.overflow = de.scrollWidth > de.clientWidth + 2;
  const ctrls = [...document.querySelectorAll("input,select,textarea")].filter(el => !el.disabled && el.type !== "hidden" && el.type !== "submit" && el.offsetParent !== null);
  if (ctrls.length) {
    out.hasInput = true;
    const el = ctrls[0], t = (el.type || "").toLowerCase();
    const v = t.includes("number") || t.includes("range") ? "10" : t === "date" ? "2026-12-25" : t === "time" ? "10:30" : t === "email" ? "a@b.com" : "test";
    try { el.value = v; el.dispatchEvent(new Event("input", {bubbles:true})); el.dispatchEvent(new Event("change", {bubbles:true})); out.interacted = true; } catch(e) { out.interacted = "ERR:" + e.message; }
  }
  const btn = [...document.querySelectorAll("button, [role=button], input[type=button]")].find(b => !b.disabled && b.offsetParent !== null);
  if (btn) { try { btn.click(); out.btnOk = true; } catch(e) { out.btnOk = "ERR:" + e.message; } }
  return JSON.stringify(out);
})()`;

const results = [];
for (const slug of slugs) {
  const url = BASE.replace(/\/?$/, "/") + slug + "/";
  const status = await httpStatus(url);
  const rec = { time: new Date().toISOString(), slug, status, consoleErrors: [], title: "", overflow: false, hasInput: false, interacted: false, btnOk: false, strict: null, ok: false };
  if (status === 200) {
    consoleErrs.length = 0;
    try {
      await send("Runtime.enable"); await send("Page.enable");
      await send("Page.navigate", { url });
      await sleep(900);
      const r = await send("Runtime.evaluate", { expression: PROBE, returnByValue: true });
      Object.assign(rec, JSON.parse(r.result?.value ?? "{}"));
      const rule = strictAll ? EXPECTS.find(t => t.slug === slug) : null;
      if (rule) {
        const sr = await send("Runtime.evaluate", { expression: STRICT_DRV(rule.js), returnByValue: true });
        rec.strict = verify(rule, sr.result?.value);
      }
    } catch (e) { rec.consoleErrors.push("PATROL-ERR:" + e.message.slice(0, 200)); }
    rec.consoleErrors = consoleErrs.slice(0, 5);
    rec.ok = rec.consoleErrors.length === 0 && rec.title && !rec.overflow && rec.interacted !== false && rec.btnOk !== false
      && (!rec.strict || rec.strict.ok);
  }
  results.push(rec);
  appendFileSync(new URL("../data/qa_log.jsonl", import.meta.url), JSON.stringify(rec) + "\n");
  console.log(`${rec.ok ? "OK " : "BUG"} ${slug} status=${status} errs=${rec.consoleErrors.length} title=${rec.title ? "y" : "N"} overflow=${rec.overflow} interact=${rec.interacted} btn=${rec.btnOk}${rec.strict ? " strict=" + (rec.strict.ok ? "PASS" : "FAIL:" + rec.strict.why) : ""}`);
}
await send("Page.navigate", { url: "about:blank" }).catch(() => {});
proc.kill();
const bugs = results.filter(r => !r.ok);
console.log("PAGE-PATROL " + JSON.stringify({ pages: results.length, bugs: bugs.length, slugs_buggy: bugs.map(b => b.slug) }));
process.exit(bugs.length ? 1 : 0);
