#!/usr/bin/env python3
"""
防偷懒自动验证器 — SYS-008 §十六 机制二 实现

用法:
  python3 auto_verify.py report.txt       # 验证文本文件
  python3 auto_verify.py data.xlsx        # 验证Excel (需 openpyxl)
  python3 auto_verify.py data.csv         # 验证CSV
  echo "输出内容" | python3 auto_verify.py -   # 管道传入

检测维度:
  1. 笼统词 — USB/电池/遥控/材质/防水 未细分 → ❌
  2. 空泛结论 — "市场不错/竞争激烈/有机会/可能/大概" → ❌
  3. 来源缺失 — 有数字无来源标记 / 来源笼统("网络/亚马逊") → ❌
  4. 统计异常 — "通用">30% / "其他">10% / Unknown>40% → ❌

退出码: 0=通过, 1=违规, 2=用法错误
"""

import re
import sys
from pathlib import Path

VAGUE = {
    "USB笼统": (
        r"(?<!\bType[\s-])USB(?![\s-]?C\b|[\s-]?接口未确认|[\s-]charging)",
        "Type-C / Micro USB / Lightning / 磁吸 / 触点 / USB接口未确认"
    ),
    "电池笼统": (
        r"(?<!锂|铅酸|干|纽扣|内置|可拆卸)[电电]池(?!包|容量|续航)",
        "锂电池 / 铅酸电池 / 干电池 / 纽扣电池 / 内置电池 / 可拆卸电池包"
    ),
    "遥控笼统": (
        r"(?<!APP|蓝牙|WiFi|2\.4G|触控|按键|语音)遥控(?!器)",
        "遥控器 / APP / 蓝牙 / WiFi / 2.4G / 触控 / 按键 / 语音"
    ),
    "材质笼统": (
        r"(?<!ABS|PP|PC|不锈钢|铝合金|硅胶|橡胶|玻璃|陶瓷)材质(?!列|字段)",
        "ABS / PP / PC / 不锈钢 / 铝合金 / 硅胶 / 橡胶 / 玻璃 / 陶瓷"
    ),
    "防水笼统": (
        r"(?<!IPX[4567]|IP6[567])防水(?!等级|保护)",
        "IPX4 / IPX5 / IPX6 / IPX7 / IP67 / 未标注"
    ),
}

HOLLOW = [
    (r"市场不错", "空泛→集中度XX%/CR5=XX/品牌数/均价$XX"),
    (r"竞争激烈", "空泛→CR5=XX%/头部品牌XX占XX%/中小品牌XX个"),
    (r"有机会|前景广阔|值得关注", "空泛→什么机会/多大市场/谁在增长"),
    (r"\b(?:可能|大概|一般来说|估计|应该是)\b", "模糊词→改为Unknown或补充来源"),
]

STATS = {"通用": 0.30, "其他": 0.10, "Unknown": 0.40, "unknown": 0.40, "待核实": 0.10}

SOURCE_MARKERS = [r"Amazon", r"卖家精灵", r"Keepa", r"ABA", r"Alexa", r"来源[:：]"]


def read_text(src):
    p = Path(src)
    if p.suffix == '.xlsx':
        try:
            import openpyxl
            wb = openpyxl.load_workbook(p, data_only=True)
            return "\n".join(
                " | ".join(str(c) if c is not None else "" for c in row)
                for ws in wb.worksheets
                for row in ws.iter_rows(values_only=True)
            )
        except ImportError:
            sys.exit("需要 openpyxl: pip install openpyxl")
    if p.suffix == '.csv':
        return p.read_text(encoding='utf-8-sig', errors='replace')
    if src == '-':
        return sys.stdin.read()
    return p.read_text(encoding='utf-8', errors='replace')


def ctx(text, start, end, w=40):
    a, b = max(0, start-w), min(len(text), end+w)
    return text[a:b].replace('\n', ' ')


def verify(src):
    text = read_text(src)
    v = {"笼统词": [], "空泛结论": [], "来源": [], "统计": []}

    for name, (pat, detail) in VAGUE.items():
        for m in re.finditer(pat, text, re.I):
            v["笼统词"].append(f"[{name}] {m.group().strip()} → 须细分: {detail}")

    for pat, detail in HOLLOW:
        for m in re.finditer(pat, text, re.I):
            v["空泛结论"].append(f"[空泛] \"{m.group().strip()}\" @ ...{ctx(text,m.start(),m.end(),30)}... → {detail}")

    numbers = re.findall(r"\b[0-9,]+(?:\.[0-9]+)?\b", text)
    has_src = any(re.search(m, text, re.I) for m in SOURCE_MARKERS)
    if len(numbers) > 5 and not has_src:
        v["来源"].append(f"检测到{len(numbers)}个数字但无来源标注(Amazon/卖家精灵/Keepa/ABA/Alexa)")

    for m in re.finditer(r"来源[:：]?\s*(?:网络|亚马逊|网上)\b", text, re.I):
        v["来源"].append(f"来源笼统 \"{m.group().strip()}\" → 须具体到产品页/参数表/五点/卖家精灵列名")

    lines = [l for l in text.split('\n') if l.strip()]
    for kw, th in STATS.items():
        cnt = sum(1 for l in lines if re.search(rf"\b{kw}\b", l, re.I))
        if lines and (r := cnt / len(lines)) > th:
            v["统计"].append(f"\"{kw}\"占比 {r:.0%} (>阈值{th:.0%}) → 须重新提取或补充")

    return v


def report(v):
    t = sum(len(x) for x in v.values())
    if t == 0:
        print("✅ 防偷懒验证通过")
        return 0
    print(f"\n{'='*60}\n🛡️ 防偷懒验证: {t}项违规\n{'='*60}")
    for cat, items in v.items():
        if items:
            print(f"\n📌 {cat} ({len(items)}):")
            for i, item in enumerate(items, 1):
                print(f"  {i}. {item[:150]}")
    print(f"\n{'='*60}\n⛔ 不通过 — {t}项需修正\n{'='*60}\n")
    return 1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("用法: auto_verify.py <文件> 或 echo '文本' | auto_verify.py -")
    sys.exit(report(verify(sys.argv[1])))