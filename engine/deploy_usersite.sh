#!/usr/bin/env bash
# Deploy the user-site repo (seyrs1985.github.io): redirect page + IndexNow key file.
# This gives the github.io HOST ROOT a controllable page, which IndexNow requires.
set -euo pipefail
cd "$(dirname "$0")/.."

export http_proxy="${http_proxy:-http://127.0.0.1:7890}"
export https_proxy="${https_proxy:-http://127.0.0.1:7890}"

TOKEN="${GITHUB_TOKEN:-}"
if [ -z "$TOKEN" ]; then TOKEN="$(git config --get tooltide.token || true)"; fi
if [ -z "$TOKEN" ]; then echo "no token (git config tooltide.token)"; exit 2; fi

TMP="$(mktemp -d)"
cp user-site/* "$TMP"/
git -C "$TMP" init -q -b main
git -C "$TMP" add -A
git -C "$TMP" -c user.name=seyrs1985 -c user.email="327587347+seyrs1985@users.noreply.github.com" commit -q -m "user site: redirect to tooltide + IndexNow key"

code="$(curl -s -o /tmp/us.json -w '%{http_code}' -X POST https://api.github.com/user/repos \
  -H "Authorization: token $TOKEN" -H 'Accept: application/vnd.github+json' \
  -d '{"name":"seyrs1985.github.io","description":"ToolTide landing","has_wiki":false,"has_projects":false,"has_issues":false,"auto_init":false}')"
case "$code" in
  201) echo "user-site repo created" ;;
  422) echo "user-site repo already exists" ;;
  *)   echo "repo create HTTP $code: $(head -c 200 /tmp/us.json)"; rm -rf "$TMP"; exit 3 ;;
esac

git -C "$TMP" -c credential.helper= push -q "https://x-access-token:${TOKEN}@github.com/seyrs1985/seyrs1985.github.io.git" main
rm -rf "$TMP"
echo "user-site pushed (Pages auto-serves from root)"
