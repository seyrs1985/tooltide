# -*- coding: utf-8 -*-
"""Submit all site URLs to IndexNow (Bing + Yandex + Seznam instant indexing).

No account needed — the key file site/<key>.txt proves ownership.
Run after every deploy. Uses https_proxy env var if set.
"""
import json
import os
import urllib.error
import urllib.request
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "docs")


def main():
    with open(os.path.join(ROOT, "config", "site.json"), encoding="utf-8") as f:
        cfg = json.load(f)
    base, key = cfg["base_url"], cfg["indexnow_key"]
    host = urlparse(base).netloc

    urls = [base]
    for dirpath, dirnames, filenames in os.walk(SITE):
        for fn in filenames:
            if fn == "index.html":
                rel = os.path.relpath(dirpath, SITE).replace("\\", "/")
                urls.append(base + (rel + "/" if rel != "." else ""))
    urls = sorted(set(urls))

    # Batch by 100: api.indexnow.org rejects the full list with
    # 403 SiteVerificationNotCompleted while a freshly-seen host is still
    # being verified asynchronously; small batches just get queued (202).
    batches = [urls[i:i + 100] for i in range(0, len(urls), 100)]
    for idx, batch in enumerate(batches, 1):
        payload = {
            "host": host,
            "key": key,
            # IndexNow requires the key file at the HOST ROOT — on the custom
            # domain that is docs/ itself; before 2026-09-25 (github.io path
            # site) it was served from the seyrs1985.github.io user-site repo.
            "keyLocation": f"https://{host}/{key}.txt",
            "urlList": batch,
        }
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                print(f"IndexNow: batch {idx}/{len(batches)} submitted {len(batch)} URLs → HTTP {resp.status}")
        except urllib.error.HTTPError as e:  # report and continue, non-fatal
            detail = e.read().decode("utf-8", "replace")[:160]
            print(f"IndexNow: batch {idx} failed (HTTP {e.code}) {detail} — will retry next deploy")
        except Exception as e:  # noqa: BLE001
            print(f"IndexNow: submit failed ({e}) — will retry next deploy")


if __name__ == "__main__":
    main()
