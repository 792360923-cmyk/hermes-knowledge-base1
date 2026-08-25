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
from datetime import datetime

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
        # ⚠️ CSV空单元格DictReader返回None，必须转空字符串防崩溃
        values = [(row.get(col_name) or '') for row in rows]
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

    # 结论段检测——锚点词去掉太宽泛的"分析"
    CONCLUSION_ANCHORS = ['结论', '建议', '发现', '总结']

    conclusion_blocks = []
    for para in text.split('\n\n'):
        if any(kw in para for kw in CONCLUSION_ANCHORS):
            # 分句：中文句号 + 英文句号(排除小数点3.14/版本1.0)
            sentences = [s.strip() for s in re.split(r'[。！？!?]|(?<!\d)\.(?!\d)', para) if len(s.strip()) > 5]
            conclusion_blocks.append(sentences)

    total_conclusion_sentences = sum(len(b) for b in conclusion_blocks)
    has_conclusion_anchor = len(conclusion_blocks) > 0

    if not has_conclusion_anchor:
        # 完全没有结论/建议/发现段落 → 明确的偷懒（BLOCKER）
        violations.append(Violation(
            "ST-NO-CONCLUSION", "table_structure", "BLOCKER",
            "全文没有「结论/建议/发现」段落",
            "全文", "必须包含结论段：数据+原因+影响+建议"
        ))
    elif total_conclusion_sentences < 3:
        # 有结论但句子不足3句 → 提示关注（WARNING，精炼结论不误杀）
        violations.append(Violation(
            "ST-CONC-SHORT", "table_structure", "WARNING",
            f"结论/建议段总句数 {total_conclusion_sentences} 句（建议≥3句）",
            "全文", "结论段建议展开：每条结论含数据+原因+影响+建议"
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

# ─── 失败案例自动写入 ──────────────────────────────────────────

KB_DIR = "/tmp/hermes-kb"
FAIL_DIR = f"{KB_DIR}/案例库/失败案例"

# 违规类别→类目映射
CATEGORY_MAP = {
    "vague_term": "field_rules（字段规则）",
    "hollow_conclusion": "source_rules（来源规则）",
    "no_source": "source_rules（来源规则）",
    "stat_anomaly": "classification_rules（分类规则）",
    "table_structure": "source_rules（来源规则）",
}

# 违规规则ID→标题前缀
TITLE_MAP = {
    "VT-USB": "USB笼统填写未细分",
    "VT-BATTERY": "电池类型笼统未细分",
    "VT-REMOTE": "遥控方式笼统未细分",
    "VT-MATERIAL": "材质笼统未细分",
    "VT-WATERPROOF": "防水等级笼统未细分",
    "HL-MARKET": "市场结论空泛未数据化",
    "HL-COMPETE": "竞争结论空泛未数据化",
    "HL-OPPORTUNITY": "机会判断空泛未数据化",
    "HL-VAGUE": "使用模糊词代替数据",
    "HL-EMPTY": "使用空话套话未下结论",
    "SRC-MISSING": "数字无来源标注",
    "SRC-VAGUE": "数据来源笼统不具体",
    "STAT-GENERIC": "分类列'通用'占比过高",
    "STAT-OTHER": "分类列'其他'占比过高",
    "STAT-UNKNOWN": "Unknown占比过高",
    "TBL-FEW-COLUMNS": "表格列数不足",
    "TBL-ERR": "CSV文件读取失败",
    "ST-NO-CONCLUSION": "全文缺少结论段",
    "ST-CONC-SHORT": "结论段过短分析不足",
    "ST-FILE-SMALL": "输出内容过少信息不足",
}

def generate_failure_case(violations: List[Violation], source_text: str = "",
                           task_name: str = "未指定任务", reporter: str = "防偷懒验证器自动捕获") -> str:
    """从违规列表生成失败案例知识卡片"""
    if not violations:
        return ""

    now = datetime.now().strftime("%Y-%m-%d")
    now_full = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 按违规类别分组
    grouped = {}
    for v in violations:
        grouped.setdefault(v.rule_id, []).append(v)

    cards = []
    seq = 1
    for rule_id, vlist in grouped.items():
        # ID: 用时间戳+序号保证唯一
        case_id = f"KB-FAIL-AUTO-{datetime.now().strftime('%Y%m%d%H%M%S')}-{seq:02d}"
        title = TITLE_MAP.get(rule_id, f"验证器拦截: {rule_id}")
        category = CATEGORY_MAP.get(vlist[0].category, "source_rules（来源规则）")

        # 收集所有违规的fix_hint去重
        fix_hints = list(dict.fromkeys(v.fix_hint for v in vlist))

        # 错误表现
        error_descriptions = []
        for v in vlist[:5]:  # 最多5条
            # 清洗 location 中的 markdown 特殊字符（反引号/管道/星号）
            loc = v.location.strip('...')
            loc = loc.replace('`', "'").replace('|', '/').replace('*', '-')
            error_descriptions.append(f"- {v.description}：`{loc[:80]}`")

        card = f"""---
id: {case_id}
title: {title}——防偷懒验证器自动捕获
type: case（案例）
category: {category}
tags: [失败案例, 防偷懒, 验证器自动捕获, {rule_id}]
roles: [Commander, Data Verifier]
status: pending（待审核）
confidence: A（验证器程序捕获+自动生成）
source: 防偷懒验证器 v1.1 自动捕获
evidence: 验证器在交付前扫描中拦截了 {len(vlist)} 条 {rule_id} 违规
created_at: {now}
updated_at: {now}
reviewed_by: 待审核
related: [SYS-008 §十六, SYS-008 §五]
---

# {title}——防偷懒验证器自动捕获

> 捕获时间: {now_full}
> 任务名称: {task_name}
> 拦截方: {reporter}

## 错误表现

{chr(10).join(error_descriptions[:5])}

## 正确做法

{chr(10).join(f'- {h}' for h in fix_hints)}

## 后果

- 违反 SYS-008 §五（禁止偷懒规则）+ §十六（防偷懒工程）
- 如不修正直接交付，用户必须返工
- 笼统/空泛/无来源的数据导致分析结论不可靠

## 适用场景

所有需要遵守 SYS-008 防偷懒规则的任务。

## 教训

{title}。验证器在交付前程序化拦截，修正后才能通过。

## 禁止再犯

是。

## 来源证据

- 防偷懒验证器 v1.1 自动捕获 ({now_full})
- 违规数: {len(vlist)} 条 ({rule_id})
- 违规类别: {category}

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| {now} | 验证器自动创建（待审核） | anti_slacker.py v1.1 |
"""
        cards.append((case_id, card))
        seq += 1

    return cards


def save_failure_cases(violations: List[Violation], source_text: str = "",
                        task_name: str = "未指定任务") -> List[str]:
    """将违规写入知识库失败案例目录，返回写入的文件路径列表"""
    saved = []
    cards = generate_failure_case(violations, source_text, task_name)
    if not cards:
        return saved

    # 确保目录存在
    fail_path = Path(FAIL_DIR)
    if not fail_path.exists():
        fail_path.mkdir(parents=True, exist_ok=True)

    for case_id, content in cards:
        filepath = fail_path / f"{case_id}.md"
        try:
            filepath.write_text(content, encoding='utf-8')
            saved.append(str(filepath))
        except Exception as e:
            print(f"⚠️ 写入失败案例失败: {filepath} — {e}", file=sys.stderr)

    return saved

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
  python3 anti_slacker.py --save-failure --task "BSR调研" report.txt  # 违规自动写入失败案例
  echo "文本" | python3 anti_slacker.py -     # 管道输入
        """
    )
    parser.add_argument("input", nargs="?", help="输入文件路径（- 为stdin）")
    parser.add_argument("--text", "-t", help="直接输入文本")
    parser.add_argument("--csv", "-c", help="CSV文件路径（表格统计检测）")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    parser.add_argument("--save-failure", "-s", action="store_true",
                        help="违规自动写入知识库失败案例目录")
    parser.add_argument("--task-name", default="未指定任务",
                        help="当前任务名称（用于失败案例标注）")
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

    # 违规自动写入失败案例（仅 BLOCKER 级）
    all_violations = [v for r in results for v in r.violations]
    blocker_violations = [v for v in all_violations if v.severity == "BLOCKER"]
    if args.save_failure and blocker_violations:
        saved = save_failure_cases(blocker_violations, text, args.task_name)
        if saved:
            print(f"\n📝 已写入 {len(saved)} 个失败案例到知识库:")
            for s in saved:
                print(f"   {s}")
            print(f"   ℹ️ 状态: pending（待审核）— 需 Commander 审核后升级")
        else:
            print(f"\n⚠️ 失败案例写入失败，检查 {FAIL_DIR} 是否可写")

    blockers = sum(1 for r in results for v in r.violations if v.severity == "BLOCKER")
    return 0 if blockers == 0 else 1

if __name__ == "__main__":
    sys.exit(main())