#!/usr/bin/env bash
# ToolTide one-command deploy:
#   build -> git commit -> create repo (first run) -> enable GitHub Pages -> push -> wait live -> IndexNow
#
# Credentials: set GITHUB_TOKEN (a PAT with `repo` scope) or store one in the
# git credential manager. First run:  GITHUB_TOKEN=ghp_xxx bash engine/deploy.sh
set -euo pipefail
cd "$(dirname "$0")/.."          # project root (ai-growth-engine)

export http_proxy="${http_proxy:-http://127.0.0.1:7890}"
export https_proxy="${https_proxy:-http://127.0.0.1:7890}"

# GitHub account to deploy under (login name, not display name).
# Resolution: $GITHUB_OWNER env > tooltide.owner config > git user.name
OWNER="$(git config --get tooltide.owner || git config --global user.name | tr -d '[:space:]')"
REPO="tooltide"
URL="https://${OWNER}.github.io/${REPO}/"
API="https://api.github.com"

echo "== 1/6 build =="
python engine/build.py | tail -1
python engine/build_games.py | tail -1

echo "== 2/6 git repository =="
if [ ! -d .git ]; then
  git init -b main -q
fi
# keep the sync folder from dragging caches around
cat > .gitignore <<'EOF'
__pycache__/
*.pyc
EOF
git add -A
git -c core.hooksPath=/dev/null commit -q -m "deploy: $(date -u '+%Y-%m-%d %H:%M UTC')" --allow-empty || true

echo "== 3/6 credentials =="
# bypass credential managers entirely: no stored creds -> no interactive hang
export GIT_TERMINAL_PROMPT=0 GCM_INTERACTIVE=never GCM_GUI_PROMPT=never
TOKEN="${GITHUB_TOKEN:-}"
if [ -z "$TOKEN" ]; then
  TOKEN="$(git config --get tooltide.token || true)"
fi
if [ -z "$TOKEN" ]; then
  cat <<'EOF'

  ✗ 未找到 GitHub token(仅首次需要)。两种方式任选:

    A. 存入全局 git 配置(永久,推荐):
       在 https://github.com/settings/tokens/new 勾选 repo 创建 PAT,然后:
       git config --global tooltide.token ghp_你的token
       bash engine/deploy.sh

    B. 临时环境变量:
       GITHUB_TOKEN=ghp_你的token bash engine/deploy.sh

EOF
  exit 2
fi

echo "== 4/6 GitHub repo =="
code="$(curl -s -o /tmp/tt_repo.json -w '%{http_code}' -X POST "$API/user/repos" \
  -H "Authorization: token $TOKEN" -H 'Accept: application/vnd.github+json' \
  -d "{\"name\":\"$REPO\",\"description\":\"Free online tools - calculators, converters, countdowns\",\"has_wiki\":false,\"has_projects\":false,\"has_issues\":true,\"auto_init\":false}")"
case "$code" in
  201) echo "   repo created: $OWNER/$REPO" ;;
  422) echo "   repo already exists" ;;
  401) echo "   ✗ token 无效或过期 (401)"; exit 3 ;;
  *)   echo "   ✗ 创建 repo 失败 HTTP $code: $(cat /tmp/tt_repo.json | head -c 300)"; exit 3 ;;
esac

echo "== 5/6 push =="
git -c credential.helper= push -q "https://x-access-token:${TOKEN}@github.com/${OWNER}/${REPO}.git" main
echo "   pushed main -> github.com/$OWNER/$REPO"

echo "== 6/6 Pages + wait for live + IndexNow =="
pcode="$(curl -s -o /tmp/tt_pages.json -w '%{http_code}' -X POST "$API/repos/$OWNER/$REPO/pages" \
  -H "Authorization: token $TOKEN" -H 'Accept: application/vnd.github+json' \
  -d '{"source":{"branch":"main","path":"/docs"}}')"
case "$pcode" in
  201) echo "   Pages enabled from /docs" ;;
  409) echo "   Pages already enabled" ;;
  *)   echo "   ⚠ Pages API HTTP $pcode: $(head -c 200 /tmp/tt_pages.json)" ;;
esac
live=0
for i in $(seq 1 24); do
  http="$(curl -s -o /dev/null -w '%{http_code}' -m 10 "$URL" || true)"
  if [ "$http" = "200" ]; then live=1; break; fi
  sleep 5
done
if [ "$live" = 1 ]; then
  echo "   ✅ 站点已上线: $URL"
else
  echo "   ⚠ 首次 Pages 构建可能需要几分钟,稍后手动检查: $URL"
fi

python engine/ping_indexnow.py || true
echo "done."
