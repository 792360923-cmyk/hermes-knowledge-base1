#!/usr/bin/env python3
"""
防偷懒自动验证器 v1.0
======================
SYS-008 §十六机制二落地 — 交付前强制扫描，不依赖LLM。
任一规则不通过→拒绝交付，返回违规清单。

用法:
    python3 anti_slacker.py <文件路径>          # 验证单个文本/CSV
    python3 anti_slacker.py --text "内容"       # 验证文本片段
    python3 anti_slacker.py --csv <CSV文件>    # 验证CSV表格
    python3 anti_slacker.py --json             # JSON格式输出（供程序调用）

退出码: 0=通过, 1=不通过(有违规), 2=运行错误
"""

import re
import sys
import csv
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field

# ─── 数据结构 ───────────────────────────────────────────────

@dataclass
class Violation:
    rule_id: str
    category: str  # 'vague_term' | 'hollow_conclusion' | 'no_source' | 'stat_anomaly' | 'table_structure'
    severity: str   # 'BLOCKER' | 'WARNING'
    description: str
    location: str   # 违规位置摘要
    fix_hint: str

@dataclass
class CheckResult:
    passed: bool
    violations: List[Violation] = field(default_factory=list)
    stats: Dict = field(default_factory=dict)

# ─── 通用工具 ───────────────────────────────────────────────

def tokenize_text(text: str) -> List[str]:
    """按中文句/段拆分，便于精确定位"""
    sentences = re.split(r'[。！？\n;；]', text)
    return [s.strip() for s in sentences if s.strip()]

def extract_numbers_with_context(text: str) -> List[Tuple[str, str]]:
    """提取所有数字及其上下文（前后各20字），返回(数字, 上下文)"""
    results = []
    for m in re.finditer(r'(?:^|(?<=[^\d]))\d[\d,.]*(?:(?=\D)|$)', text):
        start = max(0, m.start() - 20)
        end = min(len(text), m.end() + 20)
        ctx = text[start:end].replace('\n', ' ')
        results.append((m.group(), ctx))
    return results

# ─── 规则1: 笼统词扫描 ──────────────────────────────────────

VAGUE_TERM_RULES = [
    {
        "id": "VT-USB",
        "term": "USB",
        "exclude_patterns": [r"Type[-.\s]?C", r"USB[-.\s]?C", r"Micro\s*USB", r"Lightning", r"磁吸", r"触点", r"充电盒", r"USB接口未确认", r"未标注", r"VT-USB"],
        "fix": "必须写明: Type-C / Micro USB / Lightning / 磁吸 / 触点 / 充电盒 / USB接口未确认",
    },
    {
        "id": "VT-BATTERY",
        "term": "电池",
        "exclude_patterns": [r"锂电", r"锂电池", r"铅酸电池", r"干电池", r"纽扣电池", r"内置电池", r"可拆卸电池", r"电池包", r"未标注", r"VT-BATTERY"],
        "fix": "必须写明: 锂电池 / 铅酸电池 / 干电池 / 纽扣电池 / 内置电池 / 可拆卸电池包",
    },
    {
        "id": "VT-REMOTE",
        "term": "遥控",
        "exclude_patterns": [r"遥控器", r"APP", r"蓝牙", r"WiFi", r"2\.4G", r"触控", r"按键", r"语音", r"未标注", r"VT-REMOTE"],
        "fix": "必须写明: 遥控器 / APP / 蓝牙 / WiFi / 2.4G / 触控 / 按键 / 语音",
    },
    {
        "id": "VT-MATERIAL",
        "term": "材质",
        "exclude_patterns": [r"ABS", r"PP[^C]", r"PC[^B]", r"不锈钢", r"铝合金", r"硅胶", r"橡胶", r"玻璃", r"陶瓷", r"未标注", r"VT-MATERIAL"],
        "fix": "必须写明: ABS / PP / PC / 不锈钢 / 铝合金 / 硅胶 / 橡胶 / 玻璃 / 陶瓷",
    },
    {
        "id": "VT-WATERPROOF",
        "term": "防水",
        "exclude_patterns": [r"IP[Xx]?\d+", r"IP\d{2}", r"未标注", r"VT-WATERPROOF"],
        "fix": "必须写明IP等级: IPX4 / IPX5 / IPX6 / IPX7 / IP67 / 未标注",
    },
]

def check_vague_terms(text: str) -> CheckResult:
    violations = []
    for rule in VAGUE_TERM_RULES:
        # 找到所有包含该笼统词的位置
        for m in re.finditer(re.escape(rule["term"]), text):
            # 检查附近是否有排除词
            nearby = text[max(0, m.start()-30):m.end()+30]
            has_exclusion = any(re.search(pat, nearby) for pat in rule["exclude_patterns"])
            if not has_exclusion:
                # 精确定位上下文
                ctx_start = max(0, m.start() - 25)
                ctx_end = min(len(text), m.end() + 25)
                ctx = text[ctx_start:ctx_end].replace('\n', ' ').strip()
                violations.append(Violation(
                    rule_id=rule["id"],
                    category="vague_term",
                    severity="BLOCKER",
                    description=f"笼统词「{rule['term']}」未细分",
                    location=f"...{ctx}...",
                    fix_hint=rule["fix"],
                ))
    return CheckResult(
        passed=len(violations) == 0,
        violations=violations,
    )

# ─── 规则2: 空泛结论扫描 ────────────────────────────────────

HOLLOW_PHRASES = [
    ("HL-MARKET", ["市场不错", "市场很好", "市场前景好", "市场大"], "必须数据化: 市场规模$XX、增长率XX%、CR5=XX%"),
    ("HL-COMPETE", ["竞争激烈", "竞争不大", "竞争一般", "红海", "蓝海"], "必须数据化: 品牌数XX、集中度XX%、价格带XX-XX"),
    ("HL-OPPORTUNITY", ["有机会", "有前景", "前景广阔", "值得关注", "值得切入"], "必须写明: 什么机会、依据数据、切入方向、预期回报"),
    ("HL-VAGUE", ["可能", "大概", "估计", "一般来说", "应该是", "差不多"], "改为 Unknown 或补充具体来源数据"),
    ("HL-EMPTY", ["总的来说", "综上所述，这个品类", "整体来看"], "删除空话，直接用数据下结论"),
]

def check_hollow_conclusions(text: str) -> CheckResult:
    violations = []
    for rule_id, phrases, fix in HOLLOW_PHRASES:
        for phrase in phrases:
            for m in re.finditer(re.escape(phrase), text):
                ctx_start = max(0, m.start() - 20)
                ctx_end = min(len(text), m.end() + 20)
                ctx = text[ctx_start:ctx_end].replace('\n', ' ').strip()
                violations.append(Violation(
                    rule_id=rule_id,
                    category="hollow_conclusion",
                    severity="BLOCKER",
                    description=f"空泛结论: 「{phrase}」",
                    location=f"...{ctx}...",
                    fix_hint=fix,
                ))
    return CheckResult(
        passed=len(violations) == 0,
        violations=violations,
    )

# ─── 规则3: 数据来源扫描 ────────────────────────────────────

SOURCE_MARKERS = [
    "Amazon", "卖家精灵", "Keepa", "ABA", "Alexa",
    "FBA计算器", "Google Patents", "官网", "用户提供", "图片判断",
    "标题", "五点", "Product Overview", "Technical Details", "Product Information",
    "Q&A", "Review", "A+", "类目筛选",
]

VAGUE_SOURCES = ["网络", "亚马逊", "网上", "互联网", "平台"]

# 技术规格数字模式——这些行不触发来源检测
# ⚠️ Python的\b在中英文混排中失效(中文也是\w)，用(?<![a-zA-Z0-9])替代
TECH_SPEC_PATTERNS = [
    r'(?<![a-zA-Z0-9])\d+\s*mAh(?![a-zA-Z0-9])',      # 电池容量
    r'(?<![a-zA-Z0-9])IP[Xx]?\d+(?![a-zA-Z0-9])',     # 防水等级
    r'(?<![a-zA-Z0-9])\d+\s*W(?![a-zA-Z0-9])',        # 功率
    r'(?<![a-zA-Z0-9])\d+\s*V(?![a-zA-Z0-9])',        # 电压
    r'(?<![a-zA-Z0-9])\d+\s*mm(?![a-zA-Z0-9])',       # 毫米
    r'(?<![a-zA-Z0-9])\d+\s*cm(?![a-zA-Z0-9])',       # 厘米
    r'(?<![a-zA-Z0-9])\d+\s*inch(?![a-zA-Z0-9])',     # 英寸
    r'(?<![a-zA-Z0-9])\d+\s*g(?![a-zA-Z0-9])',        # 克
    r'(?<![a-zA-Z0-9])\d+\s*kg(?![a-zA-Z0-9])',       # 千克
    r'(?<![a-zA-Z0-9])\d+\s*dB(?![a-zA-Z0-9])',       # 分贝
    r'(?<![a-zA-Z0-9])\d+\s*Hz(?![a-zA-Z0-9])',       # 赫兹
    r'(?<![a-zA-Z0-9])\d+\s*RPM(?![a-zA-Z0-9])',      # 转速
    r'(?<![a-zA-Z0-9])Type[-.\s]?C(?![a-zA-Z0-9])',   # Type-C
    r'(?<![a-zA-Z0-9])USB[-.\s]?C(?![a-zA-Z0-9])',    # USB-C
    r'(?<![a-zA-Z0-9])A\d+(?![a-zA-Z0-9])',           # 电流 (A)
]

def check_sources(text: str) -> CheckResult:
    violations = []
    lines = text.split('\n')

    # 检查每行：如果有数字但没有来源标记
    for i, line in enumerate(lines):
        # 跳过纯标题行、分隔线
        if re.match(r'^[\s#\-\|=*\n]*$', line):
            continue
        # 有数字的行
        if re.search(r'\d[\d,.]*', line):
            # 如果行中所有数字都是技术规格，跳过来源检测
            # 技术规格行 = 匹配TECH_SPEC_PATTERNS + 无业务指标($/%/销量/价格/BSR/排名/件)
            is_tech_line = any(re.search(pat, line) for pat in TECH_SPEC_PATTERNS)
            has_business = bool(re.search(r'[\$%]|销量|价格|BSR|排名|件|月销|评论|评分', line))
            if is_tech_line and not has_business:
                continue

            has_source = any(marker.lower() in line.lower() for marker in SOURCE_MARKERS)
            has_vague = any(vs in line for vs in VAGUE_SOURCES)
            if has_vague and not has_source:
                # 仅有笼统来源(如"亚马逊")无具体来源(如"亚马逊标题")
                violations.append(Violation(
                    rule_id="SRC-VAGUE",
                    category="no_source",
                    severity="BLOCKER",
                    description=f"数据来源笼统（仅含'网络/亚马逊'等模糊词）",
                    location=f"行{i+1}: {line[:80]}...",
                    fix_hint="来源必须具体到: Amazon标题/五点/参数表/卖家精灵列名/Alexa对话",
                ))
            elif not has_source:
                # 有数字但完全没有来源
                violations.append(Violation(
                    rule_id="SRC-MISSING",
                    category="no_source",
                    severity="BLOCKER",
                    description=f"数字无来源标注",
                    location=f"行{i+1}: {line[:80]}...",
                    fix_hint="每个含数字的行必须标注来源: Amazon/卖家精灵/Keepa/ABA/Alexa",
                ))

    return CheckResult(
        passed=len(violations) == 0,
        violations=violations,
        stats={"total_lines": len(lines)}
    )

# ─── 规则4: 统计异常检测 (CSV/表格) ──────────────────────────

def check_csv_stats(csv_path: str) -> CheckResult:
    violations = []
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        return CheckResult(passed=False, violations=[
            Violation("TBL-ERR", "table_structure", "BLOCKER", f"无法读取CSV: {e}", csv_path, "检查文件格式")
        ])

    if not rows:
        return CheckResult(passed=True)

    # 列数检查
    col_count = len(rows[0]) if rows else 0
    if col_count < 10:
        violations.append(Violation(
            "TBL-FEW-COLUMNS", "table_structure", "BLOCKER",
            f"表格仅{col_count}列，字段明显不够（最少10列）",
            csv_path, "重新采集字段，覆盖17个字段大类"
        ))

    # 逐列统计
    for col_name in rows[0].keys():
        values = [row.get(col_name, '') for row in rows]
        total = len(values)
        generic_count = sum(1 for v in values if v.strip() == '通用')
        other_count = sum(1 for v in values if v.strip() in ('其他', '其它'))
        unknown_count = sum(1 for v in values if 'Unknown' in v or '未知' in v or '待核实' in v)

        if total > 0:
            generic_pct = generic_count / total * 100
            other_pct = other_count / total * 100
            unknown_pct = unknown_count / total * 100

            if generic_pct > 30:
                violations.append(Violation(
                    "STAT-GENERIC", "stat_anomaly", "BLOCKER",
                    f"列「{col_name}」中「通用」占比 {generic_pct:.0f}%（超过30%阈值）",
                    csv_path, "重新提取分类，拆解为多层独立列"
                ))
            if other_pct > 10:
                violations.append(Violation(
                    "STAT-OTHER", "stat_anomaly", "BLOCKER",
                    f"列「{col_name}」中「其他」占比 {other_pct:.0f}%（超过10%阈值）",
                    csv_path, "必须重新分类，减少兜底类"
                ))
            if unknown_pct > 40:
                violations.append(Violation(
                    "STAT-UNKNOWN", "stat_anomaly", "WARNING",
                    f"列「{col_name}」中 Unknown/待核实 占比 {unknown_pct:.0f}%（超过40%阈值）",
                    csv_path, "补充数据来源，降低Unknown比例"
                ))

    return CheckResult(
        passed=len(violations) == 0,
        violations=violations,
        stats={"rows": len(rows), "columns": col_count}
    )

# ─── 规则5: 结构性检查 ──────────────────────────────────────

def check_structure(text: str) -> CheckResult:
    violations = []

    # 结论段数量检查
    conclusion_sections = re.split(r'(?:结论|总结|分析|建议)', text)
    # 找结论块——查找含"结论"关键词的段
    conclusion_blocks = []
    for para in text.split('\n\n'):
        if any(kw in para for kw in ['结论', '发现', '建议', '分析']):
            sentences = [s.strip() for s in re.split(r'[。！？]', para) if len(s.strip()) > 5]
            conclusion_blocks.append(sentences)

    total_conclusion_sentences = sum(len(b) for b in conclusion_blocks)

    if total_conclusion_sentences < 3:
        violations.append(Violation(
            "ST-CONC-SHORT", "table_structure", "BLOCKER",
            f"结论/分析句总数仅{total_conclusion_sentences}句（最少3句）",
            "全文", "展开分析：每条结论须含数据+原因+影响+建议"
        ))

    # 文件大小检查（粗略）
    if len(text) < 500:
        violations.append(Violation(
            "ST-FILE-SMALL", "table_structure", "WARNING",
            f"输出内容仅{len(text)}字，可能信息不足",
            "全文", "检查是否遗漏字段或结论"
        ))

    return CheckResult(
        passed=len(violations) == 0,
        violations=violations,
        stats={"text_length": len(text), "conclusion_sentences": total_conclusion_sentences}
    )

# ─── 主运行器 ───────────────────────────────────────────────

def run_all_checks(text: str = "", csv_path: str = "") -> List[CheckResult]:
    results = []

    if text:
        results.append(check_vague_terms(text))
        results.append(check_hollow_conclusions(text))
        results.append(check_sources(text))
        results.append(check_structure(text))

    if csv_path:
        results.append(check_csv_stats(csv_path))

    return results

def format_terminal_output(results: List[CheckResult]) -> str:
    """人类可读的终端输出"""
    output = []
    total_violations = sum(len(r.violations) for r in results)
    blockers = sum(1 for r in results for v in r.violations if v.severity == "BLOCKER")
    all_passed = blockers == 0

    output.append("=" * 60)
    output.append("  防偷懒自动验证器 v1.0 — SYS-008 §十六驱动")
    output.append("=" * 60)

    for r in results:
        if r.violations:
            for v in r.violations:
                icon = "⛔" if v.severity == "BLOCKER" else "⚠️"
                output.append(f"\n{icon} [{v.rule_id}] {v.severity}")
                output.append(f"   问题: {v.description}")
                output.append(f"   位置: {v.location}")
                output.append(f"   修复: {v.fix_hint}")

    output.append(f"\n{'='*60}")
    if all_passed:
        output.append("✅ 全部通过 — 可以交付")
    else:
        output.append(f"❌ 发现 {blockers} 个阻断项 — 禁止交付，请修正后重新验证")

    output.append(f"   笼统词/空泛结论/无来源/统计异常/结构缺陷")
    output.append("=" * 60)

    return "\n".join(output)

def format_json_output(results: List[CheckResult]) -> str:
    """程序可读的JSON输出"""
    all_violations = []
    for r in results:
        for v in r.violations:
            all_violations.append({
                "rule_id": v.rule_id,
                "category": v.category,
                "severity": v.severity,
                "description": v.description,
                "location": v.location,
                "fix_hint": v.fix_hint,
            })
    blockers = sum(1 for v in all_violations if v["severity"] == "BLOCKER")
    return json.dumps({
        "passed": blockers == 0,
        "total_violations": len(all_violations),
        "blockers": sum(1 for v in all_violations if v["severity"] == "BLOCKER"),
        "warnings": sum(1 for v in all_violations if v["severity"] == "WARNING"),
        "violations": all_violations,
    }, ensure_ascii=False, indent=2)

# ─── CLI 入口 ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="防偷懒自动验证器 — 交付前强制扫描",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 anti_slacker.py report.txt          # 扫描文本文件
  python3 anti_slacker.py --text "USB充电 市场不错 约5000销量"  # 扫描文本片段
  python3 anti_slacker.py --csv data.csv      # 扫描CSV表格
  python3 anti_slacker.py --json report.txt   # JSON格式输出
  echo "文本" | python3 anti_slacker.py -     # 管道输入
        """
    )
    parser.add_argument("input", nargs="?", help="输入文件路径（- 为stdin）")
    parser.add_argument("--text", "-t", help="直接输入文本")
    parser.add_argument("--csv", "-c", help="CSV文件路径（表格统计检测）")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    args = parser.parse_args()

    text = ""
    csv_path = ""

    if args.text:
        text = args.text
    elif args.csv:
        csv_path = args.csv
        # 如果有对应的文本报告也读
        if args.input:
            try:
                text = Path(args.input).read_text(encoding='utf-8')
            except:
                pass
    elif args.input == "-":
        text = sys.stdin.read()
    elif args.input:
        p = Path(args.input)
        if p.suffix in ('.csv', '.tsv'):
            csv_path = str(p)
        else:
            text = p.read_text(encoding='utf-8')
    else:
        parser.print_help()
        return 2

    results = run_all_checks(text=text, csv_path=csv_path)

    if args.json:
        print(format_json_output(results))
    else:
        print(format_terminal_output(results))

    blockers = sum(1 for r in results for v in r.violations if v.severity == "BLOCKER")
    return 0 if blockers == 0 else 1

if __name__ == "__main__":
    sys.exit(main())