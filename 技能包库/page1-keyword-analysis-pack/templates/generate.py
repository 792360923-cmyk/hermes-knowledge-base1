#!/usr/bin/env python3
"""
=============================================================================
  第一页关键词分析 Excel 生成器 v4.0
  自包含技能包 | 改 CONFIG 区 → 运行 → 输出带折线图的 Excel
  依赖: openpyxl (自动安装)
  覆盖: Amazon US/DE/UK/FR/IT/ES/JP 全站点
=============================================================================
CONFIG 区共 5 大块需要填充:
  [1] MARKET / ASIN / OUTPUT / CURRENCY
  [2] PRODUCT 产品信息字典
  [3] KEYWORDS 列表 (8词 × 10字段)
  [4] TRENDS 趋势字典 (4-5词 × 55月) + MONTHS
  [5] 板块2-6 的文字内容 (comps/strats/concs/trend_rows/trend_yoy)
=============================================================================
"""

import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl", "-q"],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.chart import LineChart, Reference

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  CONFIG 区 — 改这里！每个新产品只改这 5 块                               ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# ── [1] 基础设置 ──────────────────────────────────────────────────────────
MARKET = "US"                         # US/DE/UK/FR/IT/ES/JP
ASIN   = "B0DJSPV9G4"                # 目标 ASIN
OUTPUT = "/tmp/B0DJSPV9G4_US_第一页.xlsx"  # 输出路径
CURRENCY = "$"                        # US→$  DE/FR/IT/ES→€  UK→£  JP→¥

# ── [2] 产品信息 (来自 asin_detail) ───────────────────────────────────────
PRODUCT = {
    "name":   "smokpub Electric Whiskey Smoker Kit, Cocktail Smoker with Heating System",
    "price":  "39.99",
    "bsr":    "#3,317 Kitchen / #2 Bar Sets",
    "rating": "4.6 / 1,314评",
    "variants": "1款 (Smoker with 6 Wood Chips)",
    "listed": "2024年11月",
    "fulfillment": "FBA",
}

# ── [3] 关键词列表 (8词 × 10字段) ────────────────────────────────────────
# 字段: [优先级标记, 关键词, 月搜索量, ABA排名, PPC, 购买率, 需供比, 商品数, SPR, 推荐度]
# 优先级标记: "🔴主推" / "🔴次推" / "🟡辅助" / "⚠️观察" / "⚠️避免"
# 颜色自动匹配: 🔴主推/次推→浅红底  🟡辅助→浅黄底  ⚠️→无色
KEYWORDS = [
    ["\U0001f534主推", "whiskey smoker kit",       "56,962", "23,083", "2.35", "1.42%", "150.3",   379, 19, "5星"],
    ["\U0001f534主推", "cocktail smoker",           "16,136", "110,774","2.74", "1.10%", "23.8",    678,  5, "5星"],
    ["\U0001f534次推", "old fashioned smoker kit",  "26,955", "61,003", "3.69", "1.30%", "73.05",   369,  8, "4星"],
    ["\U0001f7e1辅助", "bartender kit",             "54,794", "24,366", "1.39", "3.37%", "45.66",  1200, 42, "3星"],
    ["\U0001f7e1辅助", "bar accessories",           "30,087", "51,257", "1.39", "1.18%", "0.27",  111906, 9, "3星"],
    ["\u26a0\ufe0f观察", "electric smoker",         "57,093", "23,194", "6.03", "0.71%", "19.52",  2925, 10, "2星"],
    ["\u26a0\ufe0f避免", "smoker",                  "82,012", "13,036", "3.61", "0.51%", "2.90",  28240, 10, "1星"],
    ["\u26a0\ufe0f观察", "birthday gifts for men",  "191,718","3,324",  "0.85", "1.63%", "0.99", 193904, 71, "2星"],
]

# ── [4] 趋势数据 (来自 keyword_research_trends × 4-5词) ───────────────────
# 每个关键词 55 个月的 search 值 (2022.01 → 2026.07)
TRENDS = {
    "whiskey smoker kit": [6988,13007,9943,10550,17108,34051,17677,22038,30622,33127,64384,97903,30688,33483,19252,14741,5724,5271,5419,26565,14941,3721,99512,72977,30582,52333,42045,35731,39772,61934,33207,33119,41882,100052,132007,203266,90551,125670,121118,86159,80971,129729,62780,55654,59389,81079,136162,237428,79409,74268,64355,66070,79626,94776,56962],
    "cocktail smoker": [69079,176799,55131,55962,39748,51232,35776,38068,45526,41002,74371,92511,33908,33157,20518,16766,18034,31358,16927,32684,37349,34725,91675,103322,32883,25240,28214,24586,22735,26718,20214,18655,24212,20605,66532,114291,64341,58427,60619,30374,20543,18346,14156,16166,21484,24565,41715,59333,25670,21966,22887,21103,23538,20349,16136],
    "old fashioned smoker kit": [14229,16539,13871,14035,14184,16647,12580,14003,16934,16683,28740,33022,15137,17947,11670,10999,6474,16486,8967,15006,13730,22501,54633,86976,27879,28634,26631,21135,23521,33349,17172,18728,21737,53649,92590,116072,75871,85048,86150,63064,55340,82318,28962,25979,33705,48120,63849,82661,42776,40119,35417,32232,41851,42959,26955],
    "whiskey smoker": [24244,28742,15561,15333,15080,14312,8832,9707,13772,12987,20403,34094,13130,13716,6266,5543,9522,11355,7135,6649,13076,9332,26053,71716,17867,8492,7346,6148,6688,10058,5660,5671,6441,7458,18266,38551,9042,14288,13221,9242,10862,15437,9648,9004,12178,13047,30723,52174,15265,14435,15318,14711,18358,19378,12450],
}
MONTHS = ["22.01","22.02","22.03","22.04","22.05","22.06","22.07","22.08","22.09","22.10","22.11","22.12",
          "23.01","23.02","23.03","23.04","23.05","23.06","23.07","23.08","23.09","23.10","23.11","23.12",
          "24.01","24.02","24.03","24.04","24.05","24.06","24.07","24.08","24.09","24.10","24.11","24.12",
          "25.01","25.02","25.03","25.04","25.05","25.06","25.07","25.08","25.09","25.10","25.11","25.12",
          "26.01","26.02","26.03","26.04","26.05","26.06","26.07"]

# ── [5] 板块2-6 的文字内容 (AI Agent 生成, 填入下面) ─────────────────────

# 板块2: 核心对比分析 — 6维度 × 5词 (最后列=结论)
COMPS = [
    ["月搜索量", "56,962", "16,136", "26,955", "54,794", "82,012", "whiskey smoker kit最精准,57K可观"],
    ["需供比",   "150.3",  "23.8",   "73.05",  "45.66",  "2.90",   "whiskey smoker kit 150=极度蓝海"],
    ["PPC($)",   "2.35",   "2.74",   "3.69",   "1.39",   "3.61",   "酒类小众,PPC普遍$2-4,bartender kit最低"],
    ["SPR",      "19",     "5",      "8",      "42",     "10",     "old fashioned最低(8),竞争最小"],
    ["商品数",   "379",    "678",    "369",    "1,200",  "28,240", "细分商品少(<700),新品曝光机会大"],
    ["CVR",      "33.27%", "27.32%", "34.57%", "19.46%", "22.41%", "烟熏器类转化率普遍>27%"],
]

# 板块3: 三阶段切入策略 — 3阶段 × 8列
# 字段: [阶段, 目标, 主推词, 月搜索, PPC预算, 打法, 预期排名, 出单占比]
STRATS = [
    ["冷启动 1-6周", "获取初始流量+礼品场景",
     "whiskey smoker kit\nold fashioned smoker kit",
     "56,962\n26,955",
     "$2.50-3.00\n日$20-30",
     "精准+SP广告\nQ4节日季加速",
     "自然#10-20\n广告#3-8",
     "40-50%"],
    ["突破 7-20周", "拉升排名扩展覆盖",
     "whiskey smoker kit\ncocktail smoker\nold fashioned",
     "56,962\n16,136\n26,955",
     "$2.80-3.50\n日$40-60",
     "广泛+SP+SB\n礼品词组拓展",
     "自然#5-12\n广告#2-6",
     "60-75%"],
    ["放量 21周+", "稳定BSR前20 品牌认知",
     "whiskey smoker kit\nbartender kit\ncocktail smoker",
     "56,962\n54,794\n16,136",
     "$3.00-4.00\n日$60-100",
     "品牌+SB视频\n礼品场景全覆盖",
     "自然#2-8\n广告#1-4",
     "75-90%"],
]

# 板块4: 5条结论 — 每条 (标题, 四段文本, 颜色)
# 颜色: "RED"=浅红底  "YELLOW"=浅黄底  "NONE"=无底色
CONCS = [
    ("首选: whiskey smoker kit",
     "【数据】月搜索56,962 / ABA#23,083 / PPC $2.35 / 需供比150.3 / 商品379 / SPR=19 / CVR 33.27%\n"
     "【分析】类目第一精准词。需供比150=供给远不足需求。点击集中度49.7%说明头部垂直。该ASIN自然#16+广告在位,有基础权重。\n"
     "【操作】Title首位(已有); Bullet #1植入; 广告精准匹配出价 $2.50-3.00\n"
     "【预期】冷启动贡献40-50%出单,ROI 1:2-3",
     "RED"),
    ("首选长尾: old fashioned smoker kit",
     "【数据】月搜索26,955 / 需供比73.05 / 商品369 / SPR=8 / CVR 34.57%(最高)\n"
     "【分析】商品仅369,SPR=8极低。CVR 34.57%是本品类最高转化率。竞品标题密度仅8(很多竞品没用这个词)→差异化机会大。\n"
     "【操作】Title第2-3位; Search Terms必填; 广告精准匹配 $2.80-3.50\n"
     "【预期】突破期贡献25-35%出单,ROI 1:2.5-4",
     "RED"),
    ("次选: cocktail smoker",
     "【数据】月搜索16,136 / 需供比23.8 / 商品678 / SPR=5 / CVR 27.32%\n"
     "【分析】SPR=5极低——几乎没有竞品在此词上有大量评论。该ASIN自然排名较弱,机会空间大。\n"
     "【操作】Bullet #2植入; Search Terms; 广告广泛匹配 $2.50-3.00\n"
     "【预期】占15-20%出单,ROI 1:2.5-3",
     "RED"),
    ("辅助: bartender kit + bar accessories",
     "【数据】bartender kit: 月搜索54,794 / 购买率3.37% / PPC $1.39(最低) | bar accessories: 30,087 / SPR=9\n"
     "【分析】bartender kit是相邻品类(酒吧工具),搜索量大PPC低。但产品不完全匹配(烟熏器≠调酒工具)。bar accessories太泛,转化差。\n"
     "【操作】仅放Search Terms; 自动广告低价跑 $1.50-2.00; 礼品场景关联购买\n"
     "【预期】<10%出单,但拓展流量来源",
     "YELLOW"),
    ("避免: smoker(大类) / electric smoker(食物烟熏器)",
     "【数据】smoker: 82,012 / 28,240商品 / 平均价$225(食物烟熏器为主) | electric smoker: 57,093 / 平均价$270 / PPC $6.03\n"
     "【分析】这两个词主要流量来自食物烟熏器市场,与酒类烟熏器完全不同。点击浪费。\n"
     "【操作】不投放广告;仅放Search Terms末尾捡漏;否定关键词策略\n"
     "【预期】<3%出单,ROI可能为负",
     "NONE"),
]

# 板块6 趋势总结表 — 4词 × 7列
TREND_ROWS = [
    ["whiskey smoker kit",       "97,903(12月)", "203,266(12月)", "56,962", "爆发→回调→企稳", "2026.01同比-12.3%,日常约57-95K", "稳定"],
    ["cocktail smoker",          "176,799(02月)","114,291(12月)", "16,136", "暴涨→回调→反弹", "同比-60%→+14%(7月),U型底部", "反弹中"],
    ["old fashioned smoker kit", "33,022(12月)", "116,072(12月)", "26,955", "增长→回调→企稳", "2026.07同比仅-6.9%", "近均衡"],
    ["whiskey smoker",           "34,094(12月)", "38,551(12月)",  "12,450", "下降→回升→企稳", "2026.07同比+29%,年内低位运行", "稳定上升"],
]

# 板块6 趋势长文本
TREND_SUMMARY = (
    "【三阶段】①爆发期 2022-2024: whiskey smoker kit 7K→203K(+2800%),Q4季节性暴涨明显; "
    "②回调期 2025.04起: 全词-30%到-60%; "
    "③企稳期 2026: 同比跌幅快速收窄。\n"
    "【同比收窄】whiskey smoker kit: -12.3%(2026.01)→-9.3%(2026.07)收窄3pp。"
    "cocktail smoker: -60.1%(01)→+14.0%(07)已转正,反弹最强。"
    "old fashioned: -43.6%(01)→-6.9%(07)收窄37pp。"
    "whiskey smoker: +68.8%(01)→+29.0%(07),保持正增长。\n"
    "【定性】成熟稳定型市场+强季节性(Q4爆发)。当前处于淡季低位,9月起将进入爬坡期。可入场,不做爆发梦,但季节性放量价值明确。"
)

# 板块6 同比收窄表
TREND_YOY = [
    ["whiskey smoker kit",       "-12.3%", "-23.3%", "-9.3%",  "3.0pp",  "稳定企稳"],
    ["cocktail smoker",          "-60.1%", "-30.5%", "+14.0%", "74.1pp", "U底反弹"],
    ["old fashioned smoker kit", "-43.6%", "-48.9%", "-6.9%",  "36.7pp", "快速企稳"],
    ["whiskey smoker",           "+68.8%", "+59.2%", "+29.0%", "—",      "持续正增长"],
]

# 板块 1 蓝海判定注释
BLUE_OCEAN_NOTE = "蓝海判定: 需供比>20 + 商品<500 + SPR<15 + PPC<$0.40 → 本类目蓝海词:无(酒类小众品目,PPC普遍$2+)"

# 板块6 底部注释
TREND_FOOTNOTE = "注意: 2026年4月部分词同比仍负是因2025年4月基数较高,但收窄趋势确定。cocktail smoker 7月已转正增长,为最强反弹信号。"


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  以下为构建逻辑 — 一般情况下不需要修改                                   ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# ── 颜色/字体/边框 ────────────────────────────────────────────────────────
TITLE_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
TITLE_FONT = Font(name="Arial", size=14, bold=True, color="FFFFFF")
SEC_FONT   = Font(name="Arial", size=12, bold=True, color="1F4E79")
HDR_FILL   = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
HDR_FONT   = Font(name="Arial", size=10, bold=True, color="FFFFFF")
BODY_FONT  = Font(name="Arial", size=10)
BODY_SM    = Font(name="Arial", size=9)
BORDER     = Border(
    left=Side('thin'), right=Side('thin'),
    top=Side('thin'), bottom=Side('thin')
)

def _bg(h): return PatternFill(start_color=h, end_color=h, fill_type="solid")
BLUE   = _bg("D5E4F7")
GREEN  = _bg("E2EFDA")
YELLOW = _bg("FFF2CC")
RED    = _bg("FCE4D6")

# ── 构建辅助函数 ──────────────────────────────────────────────────────────
wb = Workbook()
ws = wb.active; ws.title = "第一页关键词分析"
for c, w in {'A':16,'B':30,'C':12,'D':12,'E':10,'F':10,'G':10,'H':10,'I':10,'J':12}.items():
    ws.column_dimensions[c].width = w
rw = 1  # 当前行追踪器

def _title(text):
    global rw
    ws.merge_cells(start_row=rw, start_column=1, end_row=rw, end_column=10)
    c = ws.cell(row=rw, column=1, value=text)
    c.font = TITLE_FONT; c.fill = TITLE_FILL
    c.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[rw].height = 32; rw += 1

def _sec(text, fill):
    global rw
    ws.merge_cells(start_row=rw, start_column=1, end_row=rw, end_column=10)
    c = ws.cell(row=rw, column=1, value=text)
    c.font = SEC_FONT; c.fill = fill
    c.alignment = Alignment(horizontal="left", vertical="center")
    ws.row_dimensions[rw].height = 26; rw += 1

def _hdr(headers):
    global rw
    for ci, h in enumerate(headers, 1):
        c = ws.cell(row=rw, column=ci, value=h)
        c.font = HDR_FONT; c.fill = HDR_FILL; c.border = BORDER
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    ws.row_dimensions[rw].height = 24; rw += 1

def _row(vals, fill=None, h=22):
    global rw
    for ci, v in enumerate(vals, 1):
        c = ws.cell(row=rw, column=ci, value=v)
        c.font = BODY_FONT; c.border = BORDER
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        if fill: c.fill = fill
    ws.row_dimensions[rw].height = h; rw += 1

def _long(label, text, fill=None, h=105):
    global rw
    c1 = ws.cell(row=rw, column=1, value=label)
    c1.font = Font(name="Arial", size=11, bold=True, color="1F4E79")
    c1.alignment = Alignment(vertical="top"); c1.border = BORDER
    if fill: c1.fill = fill
    ws.merge_cells(start_row=rw, start_column=2, end_row=rw, end_column=10)
    c2 = ws.cell(row=rw, column=2, value=text)
    c2.font = BODY_FONT; c2.border = BORDER
    c2.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[rw].height = h; rw += 1

def _gap(h=8):
    global rw; ws.row_dimensions[rw].height = h; rw += 1

def _info(text):
    global rw
    ws.merge_cells(start_row=rw, start_column=1, end_row=rw, end_column=10)
    ws.cell(row=rw, column=1, value=text).font = Font(name="Arial", size=9, color="666666")
    ws.row_dimensions[rw].height = 20; rw += 1

def _sum(text, h=80):
    global rw
    ws.merge_cells(start_row=rw, start_column=1, end_row=rw, end_column=10)
    c = ws.cell(row=rw, column=1, value=text)
    c.font = BODY_SM; c.border = BORDER
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[rw].height = h; rw += 1


# ── 构建 Excel ────────────────────────────────────────────────────────────
_title(f"{MARKET}站 {ASIN} · 第一页关键词分析")
_info(f"产品: {PRODUCT['name']} | 价格: {CURRENCY}{PRODUCT['price']} | "
      f"BSR: {PRODUCT['bsr']} | 评分: {PRODUCT['rating']} | "
      f"变体: {PRODUCT['variants']} | 上架: {PRODUCT['listed']} | {PRODUCT['fulfillment']}")
_gap(4)

# ── 板块1: 关键词对比数据 ──
_sec("板块1: 关键词对比数据 (2026.07)", BLUE)
_hdr(["优先级", "关键词", "月搜索量", "ABA排名", f"PPC({CURRENCY})", "购买率", "需供比", "商品数", "SPR", "推荐度"])
PRIO_FILL = {"\U0001f534主推": RED, "\U0001f534次推": RED, "\U0001f7e1辅助": YELLOW,
             "\u26a0\ufe0f观察": None, "\u26a0\ufe0f避免": None}
for kw in KEYWORDS:
    _row(kw, fill=PRIO_FILL.get(kw[0]))
_gap(4)
_sum(BLUE_OCEAN_NOTE, h=20)
_gap(8)

# ── 板块2: 核心对比分析 ──
_sec("板块2: 核心对比分析", GREEN)
_hdr(["维度", "whiskey smoker kit", "cocktail smoker", "old fash. smoker",
      "bartender kit", "smoker(大类)", "结论"])
for cvals in COMPS:
    _row(cvals)
_gap(8)

# ── 板块3: 三阶段策略 ──
_sec("板块3: 三阶段切入策略", GREEN)
_hdr(["阶段", "目标", "主推词", "月搜索", "PPC预算", "打法", "预期排名", "出单占比"])
COLORS3 = [GREEN, YELLOW, None]
for i, vals in enumerate(STRATS):
    _row(vals, fill=COLORS3[i], h=80)
_gap(8)

# ── 板块4: 结论 ──
_sec("板块4: 结论与操作建议", YELLOW)
COLOR_MAP = {"RED": RED, "YELLOW": YELLOW, "NONE": None}
for label, text, color in CONCS:
    _long(label, text, fill=COLOR_MAP[color], h=105)
_gap(6)

# ── 板块5: 数据来源 ──
_sec("板块5: 数据来源", RED)
_hdr(["项目", "数据来源", "说明"])
for s in [
    ["产品信息",  "卖家精灵 asin_detail",                f"{ASIN}, {MARKET}站"],
    ["关键词",    "卖家精灵 traffic_keyword + keyword_miner", f"{MARKET}站, 2026.07"],
    ["趋势",      "卖家精灵 keyword_research_trends",    "2022.01-2026.07 55个月"],
    ["月搜索/ABA/PPC", "卖家精灵 keyword_miner",         "month=2026.07"],
    ["供需比",    "卖家精灵 keyword_miner",              "supplyDemandRatio = 搜索量/商品数"],
    ["SPR",       "卖家精灵 keyword_miner",              "Sales per Review"],
    ["CVR",       "卖家精灵 keyword_miner",              "cvsShareRate"],
    ["参数",      "Amazon商品页",                        "价格/BSR/评分/变体"],
]:
    _row(s)
_gap(10)

# ── 板块6: 趋势分析 ──
_sec("板块6: 两年趋势分析 (2022.01-2026.07)", BLUE)
_hdr(["关键词", "2022峰值", "2024峰值", "2026.07", "2年走势", "当前状态", "判断"])
for t in TREND_ROWS:
    _row(t, h=35)
_gap(4)
_sum(TREND_SUMMARY, h=130)
_gap(4)
_sum("同比跌幅收窄趋势:", h=20)
_hdr(["关键词", "2026.01同比", "2026.04同比", "2026.07同比", "收窄(pp)", "趋势"])
for t in TREND_YOY:
    _row(t)
_gap(2)
_sum(TREND_FOOTNOTE, h=18)

wb.save(OUTPUT)
print(f"[Sheet1] Done: {OUTPUT}")


# ── 趋势图表 Sheet ────────────────────────────────────────────────────────
ws2 = wb.create_sheet("趋势图表")
kw_names = list(TRENDS.keys())
for ci, h in enumerate(["月份"] + kw_names, 1):
    c = ws2.cell(row=1, column=ci, value=h)
    c.font = Font(bold=True, name="Arial", size=10)
    c.alignment = Alignment(horizontal="center")
for ri, m in enumerate(MONTHS, 2):
    ws2.cell(row=ri, column=1, value=m).font = Font(name="Arial", size=8)
    for ki, kw in enumerate(kw_names):
        ws2.cell(row=ri, column=ki + 2, value=TRENDS[kw][ri - 2]).font = Font(name="Arial", size=8)
ws2.column_dimensions['A'].width = 8
for col in 'BCDEF':
    ws2.column_dimensions[col].width = 24

chart = LineChart()
chart.title = f"{MARKET}站 关键词搜索趋势 (2022.01-2026.07)"
chart.style = 10
chart.y_axis.title = "月搜索量"
chart.width = 38; chart.height = 20
chart.y_axis.scaling.min = 0

data_ref = Reference(ws2, min_col=2, max_col=len(kw_names) + 1, min_row=1, max_row=56)
cats_ref = Reference(ws2, min_col=1, min_row=2, max_row=56)
chart.add_data(data_ref, titles_from_data=True)
chart.set_categories(cats_ref)
for s in chart.series:
    s.graphicalProperties.line.width = 20000
ws2.add_chart(chart, "G2")
wb.save(OUTPUT)

print(f"[Final] {OUTPUT}")
print(f"   Sheets: 第一页关键词分析 + 趋势图表")
print(f"   板块: 6个 | 关键词: {len(KEYWORDS)}个 | 趋势词: {len(kw_names)}个 | 趋势月数: {len(MONTHS)}月")