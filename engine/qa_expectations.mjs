/* Shared expectation rules for calculator correctness audits.
 * Consumers: engine/math_audit.mjs (standalone full audit, local serve)
 *            engine/qa_patrol.mjs --strict (patrol-round strong asserts, live site)
 * Rule shape: { slug, want?, tol?, text?, cons?, js }
 *   js     — driver code, helpers: set(id,val) fills an input, get(id) reads element text.
 *            Return the raw output string; prefix MISSING:/ERR: on broken selectors.
 *   want   — expected numeric value (default tol 0.5%)
 *   text   — expected substring when output is not a plain number
 *   cons   — consistency check: returned "p|c|f" grams must sum to cons kcal (4/4/9)
 * Derivation discipline: fill expectations from an independent computation of the
 * documented formula, never by copying the page's own output. Note the formula in a
 * comment when the rule is added. Patrol rounds extend this file 2-3 rules per round.
 */
export const TESTS = [
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
  { slug: "speed-distance-time", text: "total time",
    js: `let m=set('sdt-d','100'); if(m)return m; m=set('sdt-s','50'); return m||get('sdt-out')+' | '+get('sdt-unit');` },
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
  // ---- extended coverage (night of 2026-09-19) ----
  { slug: "grade-calculator", want: 85,
    js: `let m=set('gr-earned','85'); if(m)return m; m=set('gr-total','100'); return m||get('gr-pct');` },
  { slug: "half-calculator", text: "3-1/2",
    js: `const m=set('hf-in','7'); return m||get('hf-out');` },
  { slug: "unit-price-calculator", want: 0.16,
    js: `let m=set('up-ap','2.50'); if(m)return m; m=set('up-aq','10'); if(m)return m; m=set('up-bp','4.00'); if(m)return m; m=set('up-bq','25'); return m||get('up-ub');` },
  { slug: "water-intake-calculator", want: 2.31,
    js: `let m=set('wt-kg','70'); if(m)return m; m=set('wt-ex','0'); return m||get('wt-out');` },
  { slug: "tdee-calculator", want: 1730,
    js: `let m=set('td-sex','m'); if(m)return m; m=set('td-age','30'); if(m)return m; m=set('td-h','180'); if(m)return m; m=set('td-w','75'); return m||get('td-bmr');` },
  { slug: "macro-calculator", cons: 2000,
    js: `let m=set('mc-cal','2000'); if(m)return m; return [get('mc-pg'),get('mc-cg'),get('mc-fg')].join('|');` },
  { slug: "standard-deviation-calculator", want: 2.138,
    js: `const m=set('sd-in','2,4,4,4,5,5,7,9'); return m||get('sd-out');` },
  { slug: "debt-payoff-calculator", want: 10,
    js: `let m=set('dp-b','1000'); if(m)return m; m=set('dp-r','0'); if(m)return m; m=set('dp-m','100'); return m||get('dp-out');` },
  { slug: "cagr-calculator", want: 14.87, tol: 0.01,
    js: `let m=set('cg-b','100'); if(m)return m; m=set('cg-e','200'); if(m)return m; m=set('cg-y','5'); return m||get('cg-out');` },
  // unitconv family sample: expected = (7 * factor).toFixed(dec)
  { slug: "liters-to-ml", want: 7000, js: `const m=set('uc-a','7'); return m||get('uc-r');` },
  { slug: "inches-to-feet", want: 0.583, js: `const m=set('uc-a','7'); return m||get('uc-r');` },
  { slug: "gallons-to-quarts", want: 28, js: `const m=set('uc-a','7'); return m||get('uc-r');` },
  { slug: "mm-to-inches", want: 0.28, js: `const m=set('uc-a','7'); return m||get('uc-r');` },
  { slug: "ounces-to-grams", want: 198.45, js: `const m=set('uc-a','7'); return m||get('uc-r');` },
  { slug: "grams-to-kilograms", want: 0.01, js: `const m=set('uc-a','7'); return m||get('uc-r');` },
  // money-adjacent batch (trust-critical)
  { slug: "amortization-schedule", want: 599.55, tol: 0.01,
    js: `let m=set('am-p','20000'); if(m)return m; m=set('am-r','5'); if(m)return m; m=set('am-y','3'); return m||get('am-out');` },
  { slug: "salary-to-hourly", want: 25,
    js: `let m=set('sal-yr','52000'); if(m)return m; m=set('sal-hpw','40'); if(m)return m; m=set('sal-wpy','52'); return m||get('sal-h');` },
  { slug: "overtime-pay-calculator", want: 950,
    js: `let m=set('ot-r','20'); if(m)return m; m=set('ot-h','45'); if(m)return m; m=set('ot-t','40'); if(m)return m; m=set('ot-m','1.5'); return m||get('ot-out');` },
  { slug: "inflation-calculator", want: 246.37, tol: 0.01,
    js: `let m=set('inf-a','100'); if(m)return m; m=set('inf-f','1990'); if(m)return m; m=set('inf-t','2025'); return m||get('inf-out');` },
  { slug: "break-even-calculator", want: 100,
    js: `let m=set('be-f','1000'); if(m)return m; m=set('be-p','25'); if(m)return m; m=set('be-v','15'); return m||get('be-out');` },
];

export function verify(t, raw) {
  raw = String(raw ?? "NO-VALUE");
  if (/^(MISSING|ERR)/.test(raw)) return { ok: false, why: raw };
  if (t.text) {
    const ok = raw.includes(t.text);
    return { ok, why: ok ? "" : `expected text "${t.text}"`, raw };
  }
  if (t.cons) {
    const [pg, cg, fg] = raw.split("|").map(s => parseFloat(String(s).replace(/[^\d.]/g, "")));
    const sum = (pg || 0) * 4 + (cg || 0) * 4 + (fg || 0) * 9;
    const ok = isFinite(sum) && Math.abs(sum - t.cons) <= t.cons * 0.01;
    return { ok, why: ok ? "" : `grams sum to ${sum}, want ${t.cons}`, raw };
  }
  const num = parseFloat(raw.replace(/[^\d.,-]/g, "").replace(/,/g, "").match(/-?\d+(\.\d+)?/)?.[0]);
  const tol = t.tol ?? 0.005;
  const ok = isFinite(num) && Math.abs(num - t.want) <= Math.abs(t.want) * tol + 1e-9;
  return { ok, why: ok ? "" : `got ${num}, want ${t.want}`, raw };
}
