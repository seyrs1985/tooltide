# -*- coding: utf-8 -*-
"""R120 修复:tools.py 里 JS 的 \\uXXXX 转义被 Python 编译期解析成孤立代理对,替换为真实 emoji。"""
import io

p = r"I:\BaiduSyncdisk\Drill\数据报告\ai-growth-engine\engine\tools.py"
s = io.open(p, encoding="utf-8").read()

pairs = {
    "\\uD83C\\uDF11": "\U0001F311",
    "\\uD83C\\uDF12": "\U0001F312",
    "\\uD83C\\uDF13": "\U0001F313",
    "\\uD83C\\uDF14": "\U0001F314",
    "\\uD83C\\uDF15": "\U0001F315",
    "\\uD83C\\uDF16": "\U0001F316",
    "\\uD83C\\uDF17": "\U0001F317",
    "\\uD83C\\uDF18": "\U0001F318",
}
for k, v in pairs.items():
    assert s.count(k) == 3, (k, s.count(k))
    s = s.replace(k, v)

io.open(p, "w", encoding="utf-8", newline="").write(s)
import ast
ast.parse(s)
print("escapes -> real emoji, ast ok")
