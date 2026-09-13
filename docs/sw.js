/* ToolTide service worker — offline fallback + fast repeat visits. */
var BASE = "/tooltide/";
var CACHE = "tooltide-v1";
var PRECACHE = [BASE, BASE + "i18n.js", BASE + "manifest.webmanifest",
  BASE + "favicon.ico", BASE + "apple-touch-icon.png",
  BASE + "icon-192.png", BASE + "icon-512.png", BASE + "opensearch.xml"];
self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) {
    return c.addAll(PRECACHE);
  }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (keys) {
    return Promise.all(keys.map(function (k) {
      return k === CACHE ? null : caches.delete(k);
    }));
  }).then(function () { return self.clients.claim(); }));
});
self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;
  var url = new URL(req.url);
  if (url.origin !== location.origin || url.pathname.indexOf(BASE) !== 0) return;
  if (req.headers.get("range")) return;
  if (req.mode === "navigate") {
    e.respondWith(fetch(req).then(function (res) {
      if (res.ok) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(url.pathname, copy); });
      }
      return res;
    }).catch(function () {
      return caches.match(url.pathname).then(function (hit) {
        return hit || caches.match(BASE);
      });
    }));
    return;
  }
  e.respondWith(caches.match(req).then(function (hit) {
    var net = fetch(req).then(function (res) {
      if (res.ok) {
        var copy = res.clone();
        caches.open(CACHE).then(function (c) { c.put(req, copy); });
      }
      return res;
    }).catch(function () { return hit; });
    return hit || net;
  }));
});
