#!/usr/bin/env python3
"""
防偷懒验证器回归测试 v1.0
==========================
全量回归测试，每次修改 anti_slacker.py 后必须跑通。
本测试脚本经过严格校正，测试期望值全部经过人工核实。

用法: python3 test_anti_slacker.py
退出码: 0=全过, 1=有失败
"""

import sys, csv, tempfile, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from anti_slacker import *

PASS = 0
FAIL = 0

def T(name, actual, expected, detail=""):
    global PASS, FAIL
    ok = (actual == expected) or (expected is True and actual) or (expected is False and not actual)
    if ok:
        PASS += 1
        print(f"✅ {name}")
    else:
        FAIL += 1
        print(f"❌ {name}: 期望 {expected} 实际 {actual} {detail}")

def make_csv(rows_2d):
    """正确生成CSV——rows_2d是二维列表"""
    p = tempfile.mktemp(suffix='.csv')
    with open(p, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['产品类型', '充电方式', '电池类型', '价格', '月销'])
        for r in rows_2d:
            w.writerow(r)
    return p

# ════════════════════════════════════════
# 1. 笼统词 VT-USB
# ════════════════════════════════════════
print("\n─── VT-USB ───")
T("USB笼统", len(check_vague_terms("USB充电").violations), 1)
T("Type-C合规", len(check_vague_terms("Type-C充电").violations), 0)
T("USB-C合规", len(check_vague_terms("USB-C接口").violations), 0)
T("Micro USB合规", len(check_vague_terms("Micro USB接口").violations), 0)
T("Lightning合规", len(check_vague_terms("Lightning接口").violations), 0)
T("磁吸合规", len(check_vague_terms("磁吸充电").violations), 0)
T("触点合规", len(check_vague_terms("触点充电").violations), 0)
T("充电盒合规", len(check_vague_terms("充电盒充电").violations), 0)
T("USB接口未确认合规", len(check_vague_terms("USB接口未确认").violations), 0)
T("规则ID不误触发", len(check_vague_terms("VT-USB VT-BATTERY VT-REMOTE").violations), 0)

# ════════════════════════════════════════
# 2. 笼统词 VT-BATTERY / VT-REMOTE / VT-MATERIAL / VT-WATERPROOF
# ════════════════════════════════════════
print("\n─── 其他笼统词 ───")
T("电池笼统", len(check_vague_terms("电池供电").violations), 1)
T("锂电池合规", len(check_vague_terms("锂电池供电").violations), 0)
T("电池未标注合规", len(check_vague_terms("电池未标注").violations), 0)
T("遥控笼统", len(check_vague_terms("遥控操作").violations), 1)
T("APP控制合规", len(check_vague_terms("APP控制").violations), 0)
T("遥控未标注合规", len(check_vague_terms("遥控未标注").violations), 0)
T("材质笼统", len(check_vague_terms("材质不错").violations), 1)
T("ABS材质合规", len(check_vague_terms("ABS材质").violations), 0)
T("防水笼统", len(check_vague_terms("防水设计").violations), 1)
T("IPX7合规", len(check_vague_terms("IPX7防水").violations), 0)
T("防水未标注合规", len(check_vague_terms("防水未标注").violations), 0)

# ════════════════════════════════════════
# 3. 空泛结论
# ════════════════════════════════════════
print("\n─── 空泛结论 ───")
for phrase in ["市场不错", "竞争激烈", "有机会", "值得关注", "可能", "大概",
               "估计", "一般来说", "应该是", "差不多", "红海", "蓝海",
               "前景广阔", "总的来说"]:
    T(f"「{phrase}」拦截", len(check_hollow_conclusions(phrase).violations) >= 1, True)

# ════════════════════════════════════════
# 4. 来源检测
# ════════════════════════════════════════
print("\n─── 来源检测 ───")
T("数字+Amazon通过", len(check_sources("月销5000(Amazon标题)").violations), 0)
T("数字+卖家精灵通过", len(check_sources("BSR#12(卖家精灵)").violations), 0)
T("纯数字无来源拦截", len(check_sources("销量5000件").violations) > 0, True)
T("仅亚马逊→SRC-VAGUE", any(v.rule_id == "SRC-VAGUE" for v in check_sources("销量5000(亚马逊来源)").violations), True)
T("亚马逊标题→通过", check_sources("销量5000(亚马逊标题)").passed, True)
T("技术规格跳过来源", check_sources("内置锂电池5000mAh").passed, True)

# ════════════════════════════════════════
# 5. CSV统计
# ════════════════════════════════════════
print("\n─── CSV统计 ───")
# 通用90%拦截
r = check_csv_stats(make_csv([['通用', 'USB', '电池', '19.99', '500']] * 9 + [['电动', 'Type-C', '锂电池', '39.99', '800']]))
T("通用90%拦截", any(v.rule_id == "STAT-GENERIC" for v in r.violations), True)

# 通用30%通过（阈值>30%，等于不触发）
r = check_csv_stats(make_csv([['通用', 'USB', '电池', '19.99', '500']] * 3 + [['电动', 'Type-C', '锂电池', '39.99', '800']] * 7))
T("通用30%通过", any(v.rule_id == "STAT-GENERIC" for v in r.violations), False)

# 其他10%通过（阈值>10%）
r = check_csv_stats(make_csv([['其他', '-', '-', '-', '-']] * 10 + [['电动', 'Type-C', '锂电池', '39.99', '800']] * 90))
T("其他10%通过", any(v.rule_id == "STAT-OTHER" for v in r.violations), False)

# Unknown41% WARNING
r = check_csv_stats(make_csv([['未知', '-', '-', '-', '-']] * 41 + [['电动', 'Type-C', '锂电池', '39.99', '800']] * 59))
T("Unknown41%=WARNING", any(v.rule_id == "STAT-UNKNOWN" and v.severity == "WARNING" for v in r.violations), True)

# 空单元格不崩溃
r = check_csv_stats(make_csv([['', '', '', '', '']] * 5 + [['电动', 'Type-C', '锂电池', '39.99', '800']] * 5))
T("空单元格CSV不崩溃", isinstance(r, CheckResult), True)

# 列数不足
r = check_csv_stats(make_csv([['电动', 'Type-C', '锂电池', '39.99', '800']] * 3))
# 上面5列，需要构造更少的列
import csv as _csv
p = tempfile.mktemp(suffix='.csv')
with open(p, 'w', newline='') as f:
    w = _csv.writer(f)
    w.writerow(['产品类型', '价格'])
    for _ in range(3):
        w.writerow(['电动', '19.99'])
r = check_csv_stats(p); os.unlink(p)
T("3列拦截", any(v.rule_id == "TBL-FEW-COLUMNS" for v in r.violations), True)

# ════════════════════════════════════════
# 6. 结构检测
# ════════════════════════════════════════
print("\n─── 结构检测 ───")
T("完全无结论→BLOCKER", any(v.rule_id == "ST-NO-CONCLUSION" and v.severity == "BLOCKER" for v in check_structure("USB充电，电池，市场不错。月销5000。").violations), True)
T("精炼结论→WARNING", any(v.rule_id == "ST-CONC-SHORT" and v.severity == "WARNING" for v in check_structure("结论：CR5=78%。建议：$29.99定价。").violations), True)
T("'分析'不误触发", any(v.rule_id == "ST-CONC-SHORT" for v in check_structure("数据分析显示CR5=78%。").violations), False)
T("超短文本WARNING", any(v.rule_id == "ST-FILE-SMALL" for v in check_structure("Hi").violations), True)

# ════════════════════════════════════════
# 7. 综合场景
# ════════════════════════════════════════
print("\n─── 综合场景 ───")
bad = "USB充电，电池，遥控，市场不错，竞争激烈，有机会。大概月销5000。"
bad_b = sum(1 for r in run_all_checks(text=bad) for v in r.violations if v.severity == "BLOCKER")
T(f"偷懒报告→{bad_b} BLOCKER (≥8)", bad_b >= 8, True)

good = """产品采用Type-C有线充电，内置锂电池5000mAh。
控制方式：APP遥控+蓝牙连接+触控按键。
材质：ABS+PC外壳，IPX7防水等级。
结论：市场CR5=78%，头部品牌A占32%，价格带$15-$45集中(Amazon BSR数据)。
建议：$29.99定价+IPX7防水+APP控制差异化，瞄准$25-$35空白带(卖家精灵价格分析)。
发现：新品占比18%增速快，月销约12000件(卖家精灵2026-08月销数据)。"""
good_b = sum(1 for r in run_all_checks(text=good) for v in r.violations if v.severity == "BLOCKER")
T(f"合规报告→{good_b} BLOCKER (应0)", good_b, 0)

# ════════════════════════════════════════
# 8. JSON输出 + 失败案例生成
# ════════════════════════════════════════
print("\n─── JSON + 失败案例 ───")
d = json.loads(format_json_output(run_all_checks(text="USB充电")))
T("JSON可解析", isinstance(d, dict) and "passed" in d, True)

vs = [Violation("VT-USB", "vague_term", "BLOCKER", "USB未细分", "loc", "fix")]
cards = generate_failure_case(vs, "src", "task")
T("失败案例生成", len(cards), 1)
T("案例格式完整", all(k in cards[0][1] for k in ["错误表现", "正确做法", "禁止再犯", "来源证据"]), True)

print(f"\n{'=' * 55}")
print(f"结果: {PASS} 通过 / {FAIL} 失败 / {PASS + FAIL} 项")
print(f"{'=' * 55}")
sys.exit(1 if FAIL > 0 else 0)
