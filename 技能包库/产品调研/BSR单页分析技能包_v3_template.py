#!/usr/bin/env python3
"""
BSR100 单页分析模板 — v1.1（通用版，支持3类目）
用法：修改"用户配置区"，然后 python3 template.py
输入：卖家精灵导出的 BSR{类目名}Current-100-US-{日期}.xlsx
输出：BSR_{类目名}_单页分析.xlsx

支持类目（CATEGORY_TYPE 选择）：
  "bands"  = 替换表带（适配设备/材质/外观/扣环/佩戴/防水）
  "smoker" = 威士忌烟熏器（电动/火枪/材质/充电/LED/风扇/木屑/冷烟/喷枪）
  "shaker" = 鸡尾酒调酒器（套装/冰石/件数/材质/颜色/支架/摇酒器/配件）
"""
import pandas as pd, os, re, requests, sys, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from PIL import Image
from io import BytesIO

# ══════════════════ 用户配置区 ══════════════════
EXCEL_PATH   = "/root/.hermes/cache/documents/doc_xxx.xlsx"  # BSR前100文件路径
CATEGORY_TYPE = "bands"   # "bands" | "smoker" | "shaker"
TARGET_ASIN  = "B0XXXXXXX"    # 目标ASIN
# 目标赛道（同此值的才标蓝）— 按类目填：
#   bands:  TARGET_VALUE = "Whoop 5.0"（适配设备）
#   smoker: TARGET_VALUE = "电动烟熏器"（类型）
#   shaker: TARGET_VALUE = "摇酒器套装"（类型）
TARGET_VALUE = "Whoop 5.0"
CATEGORY_NAME = "替换表带"
OUTPUT = "/tmp/BSR_分析结果.xlsx"

# ══════════════════ 汇率 ══════════════════
def get_rate():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD", timeout=5)
        return float(r.json()["rates"]["CNY"])
    except:
        return 7.25
EXCHANGE = get_rate()
TODAY = datetime.datetime.now().strftime("%Y-%m-%d")
print(f"汇率: 1 USD = {EXCHANGE} CNY")

# ══════════════════ 数据加载 ══════════════════
df = pd.read_excel(EXCEL_PATH, engine='openpyxl')

def gv(r, c):
    for k in [c, c.lower()]:
        if k in r: v = r[k]; return None if pd.isna(v) else v
    return None

official_brands = ['whoop','fitbit','apple','garmin','adidas','nike','under armour','google']

# ══════════════════════════════════════════════════════════════
# 类目A: 替换表带 (bands)
# ══════════════════════════════════════════════════════════════
def classify_bands(row):
    title = str(gv(row,'商品标题') or '').lower()
    bullets = str(gv(row,'产品卖点') or '').lower()
    params = str(gv(row,'详细参数') or '').lower()
    full = title + ' ' + bullets + ' ' + params
    brand = str(gv(row,'品牌') or '').lower().strip()
    d = {}
    # 设备
    if 'whoop 5.0' in full: d['device'] = 'Whoop 5.0'
    elif 'fitbit versa 4' in full or 'fitbit sense 2' in full: d['device'] = 'Fitbit Versa4/Sense2'
    elif 'fitbit versa 3' in full or 'fitbit sense' in title: d['device'] = 'Fitbit Versa3/Sense'
    elif 'fitbit charge 6' in full: d['device'] = 'Fitbit Charge6'
    elif 'fitbit charge 5' in full: d['device'] = 'Fitbit Charge5'
    elif 'fitbit inspire 3' in full: d['device'] = 'Fitbit Inspire3'
    elif 'fitbit air' in full or 'google fitbit air' in full: d['device'] = 'Google Fitbit Air'
    elif 'garmin' in full: d['device'] = 'Garmin通用'
    elif 'apple watch' in full: d['device'] = 'Apple Watch'
    elif 'hume' in full: d['device'] = 'Hume 2.0'
    elif 'amazfit' in full: d['device'] = 'Amazfit Helio'
    elif 'casio' in full: d['device'] = 'Casio'
    elif brand in ['adidas','nike','under armour']: d['device'] = '运动腕带'
    else: d['device'] = '其他'
    # 材质 16细分
    if 'lace' in title and 'silicone' in full: m = '硅胶蕾丝(Lace Silicone)'
    elif 'silicone' in full:
        if 'soft' in full: m = '硅胶软质(Soft Silicone)'
        elif 'sport' in title: m = '硅胶运动(Sport Silicone)'
        elif 'ultra-soft' in full: m = '硅胶超软(Ultra-Soft Silicone)'
        else: m = '硅胶标准(Silicone)'
    elif 'nylon' in full or 'woven' in full or 'knit' in full:
        if 'braided' in full: m = '尼龙编织(Braided Nylon)'
        elif 'elastic' in full: m = '尼龙弹力(Elastic Nylon)'
        elif 'woven' in full or 'knit' in full: m = '尼龙针织(Woven/Knit Nylon)'
        elif 'bicep' in full: m = '尼龙臂带(Bicep Nylon)'
        elif 'loop' in title: m = '尼龙回环(Sport Loop Nylon)'
        elif 'superknit' in full or 'super knit' in full: m = '尼龙高端(SuperKnit Nylon)'
        else: m = '尼龙标准(Nylon)'
    elif 'stainless steel' in full or 'metal mesh' in full:
        if 'mesh' in full: m = '不锈钢编织网(Metal Mesh)'
        elif 'milanese' in full: m = '不锈钢米兰尼斯(Milanese)'
        elif 'x-shape' in title: m = '不锈钢X型(X-Shape Metal)'
        elif 'floral' in full: m = '不锈钢花纹(Floral Metal)'
        else: m = '不锈钢标准(Stainless Steel)'
    elif 'leather' in full: m = '皮革(Leather)'
    elif 'tpu' in full or 'elastomer' in full: m = 'TPU弹性体(TPU/Elastomer)'
    elif 'elastic' in full: m = '弹力松紧(Elastic)'
    elif 'terry' in full or 'cotton' in full: m = '棉质毛巾(Cotton Terry)'
    else: m = '未标注'
    d['material'] = m
    # 外观 10种
    if 'lace' in title and 'silicone' in full: a = '蕾丝镂空(Lace Cutout)'
    elif 'braided' in full: a = '编织纹理(Braided)'
    elif 'woven' in full or 'knit' in full: a = '针织纹理(Woven/Knit)'
    elif 'metal mesh' in full: a = '金属编网(Metal Mesh)'
    elif 'milanese' in full: a = '米兰尼斯(Milanese Loop)'
    elif 'floral' in full or 'engraved' in full: a = '花纹雕刻(Floral/Engraved)'
    elif 'loop' in title: a = '回环式(Loop Style)'
    elif 'two-tone' in title: a = '双色拼接(Two-Tone)'
    else: a = '纯色素面(Solid)'
    d['appearance'] = a
    # 扣环 7种
    if 'hook & loop' in full or 'hook and loop' in full: c = '魔术贴(Hook&Loop)'
    elif 'magnetic' in full: c = '磁吸扣(Magnetic)'
    elif 'buckle' in full and 'pin' in full: c = '针扣(Pin Buckle)'
    elif 'buckle' in full: c = '卡扣(Buckle)'
    elif 'pin' in full and 'tuck' in full: c = '针扣(Pin&Tuck)'
    elif 'clasp' in full: c = '扣环(Clasp)'
    else: c = '未标注'
    d['clasp'] = c
    d['brand_type'] = '官方原装' if brand in official_brands else '第三方'
    d['position'] = '臂带(Bicep)' if 'bicep' in full else '腕带(Wrist)'
    if 'waterproof' in full: w = '防水(Waterproof)'
    elif 'water resistant' in full: w = '抗水(WR)'
    elif 'sweatproof' in full: w = '防汗(Sweatproof)'
    else: w = '未标注'
    d['waterproof'] = w
    m = re.search(r'(\d+)\s*pack', full); d['pack'] = int(m.group(1)) if m else 1
    m = re.search(r'(\d+)\s*mm', full); d['width'] = f"{m.group(1)}mm" if m else '未标注'
    d['is_competitor'] = (d['device'] == TARGET_VALUE)
    return d

def cn_title_bands(row):
    brand = str(gv(row,'品牌') or '')
    device = row.get('device','')
    mat = str(row.get('material','')).split('(')[0]
    app = str(row.get('appearance','')).split('(')[0]
    pack = row.get('pack',1)
    parts = [f"[{device}]", brand]
    if pack > 1: parts.append(f"{pack}件装")
    parts.append(f"{mat}{app}")
    return ' '.join(parts)

def selling_bands(row):
    full = (str(gv(row,'商品标题') or '') + ' ' + str(gv(row,'产品卖点') or '')).lower()
    pts = []
    for en,cn in {'soft':'柔软','breathable':'透气','stretchy':'弹力','waterproof':'防水',
                  'sweatproof':'防汗','washable':'可水洗','quick-dry':'速干','lightweight':'超轻',
                  'durable':'耐用','skin-friendly':'亲肤','easy install':'易安装','no tools':'免工具',
                  'adjustable':'可调节','magnetic':'磁吸扣','gift':'礼盒','lace':'蕾丝镂空',
                  'floral':'花纹雕刻','engraved':'雕刻'}.items():
        if en in full: pts.append(cn)
    m = re.search(r'(\d+)\s*pack', full)
    if m and int(m.group(1)) >= 3: pts.append('多件套装')
    return '，'.join(pts[:6]) if pts else '—'

BANDS_HEADERS = [
    "#","图","中文标题","品牌","适配设备","材质细分","外观类型","扣环",
    "价格$","Prime$","Coupon","评分","评数","上架","ASIN","链接",
    "月销","月销$","月销¥","包装","佩戴","防水","宽度",
    "品牌类型","AC","BSeller","变体","天数","LQS","FBA","运费$","A+","视频","卖点(中文)"
]
BANDS_ROW = lambda row, idx, asin, is_tgt: [
    idx+1, None, row.get('cn_title',''), gv(row,'品牌'),
    row.get('device',''), row.get('material',''), row.get('appearance',''), row.get('clasp',''),
    f"${gv(row,'价格($)'):,.2f}" if gv(row,'价格($)') and not pd.isna(gv(row,'价格($)')) else '',
    f"${gv(row,'Prime价格($)'):,.2f}" if gv(row,'Prime价格($)') and not pd.isna(gv(row,'Prime价格($)')) else '—',
    str(gv(row,'Coupon') or '—'), gv(row,'评分'),
    f"{int(gv(row,'评分数')):,}" if gv(row,'评分数') and not pd.isna(gv(row,'评分数')) else '',
    str(gv(row,'上架时间') or '')[:10], asin,
    gv(row,'商品详情页链接') or f"https://www.amazon.com/dp/{asin}",
    f"{int(gv(row,'月销量')):,}" if gv(row,'月销量') and not pd.isna(gv(row,'月销量')) else '',
    f"${gv(row,'月销售额($)'):,.0f}" if gv(row,'月销售额($)') and not pd.isna(gv(row,'月销售额($)')) else '',
    f"¥{gv(row,'月销售额($)')*EXCHANGE:,.0f}" if gv(row,'月销售额($)') and not pd.isna(gv(row,'月销售额($)')) else '',
    str(row.get('pack','1')), row.get('position',''), row.get('waterproof',''), row.get('width',''),
    row.get('brand_type',''),
    '✅' if str(gv(row,"Amazon's Choice")or'').upper()=='Y' else '',
    '✅' if str(gv(row,'Best Seller标识')or'').upper()=='Y' else '',
    str(gv(row,'变体数') or '1'), str(gv(row,'上架天数') or ''), str(gv(row,'LQS') or ''),
    str(gv(row,'配送方式') or ''),
    f"${gv(row,'FBA($)'):,.2f}" if gv(row,'FBA($)') and not pd.isna(gv(row,'FBA($)')) else '—',
    '✅' if str(gv(row,'A+页面')or'').upper()=='Y' else '',
    '✅' if str(gv(row,'视频介绍')or'').upper()=='Y' else '',
    row.get('卖点中文',''),
]

# ══════════════════════════════════════════════════════════════
# 类目B: 威士忌烟熏器 (smoker)
# ══════════════════════════════════════════════════════════════
def classify_smoker(row):
    title = str(gv(row,'商品标题') or '').lower()
    bullets = str(gv(row,'产品卖点') or '').lower()
    params = str(gv(row,'详细参数') or '').lower()
    full = title + ' ' + bullets + ' ' + params
    brand = str(gv(row,'品牌') or '').lower().strip()
    d = {}
    # 类型
    if 'electric' in title or 'rechargeable' in title: d['type'] = '电动烟熏器'
    elif 'torch' in full: d['type'] = '火枪烟熏器'
    else: d['type'] = '烟熏器'
    # 材质
    if 'stainless steel' in full: m = '不锈钢'
    elif 'wood' in full or 'mahogany' in full or 'walnut' in full: m = '木质'
    elif 'oak' in full: m = '橡木'
    elif 'plastic' in full or 'abs' in full: m = '塑料'
    else: m = '未标注'
    d['material'] = m
    # 充电方式（强制细分，禁止笼统USB）
    if 'usb-c' in full or 'type-c' in full or 'type c' in full: d['充电'] = 'USB-C'
    elif 'usb' in full: d['充电'] = 'USB(接口未确认)'
    else: d['充电'] = '未标注'
    # 功能标记
    d['LED'] = '✅' if 'led' in full else ''
    d['显示屏'] = '✅' if ('display' in full or 'screen' in full) else ''
    d['安全盖'] = '✅' if ('magnetic' in full or 'safety cover' in full or 'auto' in full) else ''
    d['风扇'] = '✅' if 'fan' in full else ''
    # 木屑数
    m = re.search(r'(\d+)\s*(wood chip|chips|flavor|flavors)', full)
    d['木屑'] = f"{m.group(1)}种" if m else '未标注'
    d['冷烟'] = '✅' if 'cold smoke' in full else ''
    d['含喷枪'] = '✅' if 'torch' in full else ''
    d['过滤嘴'] = '✅' if ('filter' in full or 'mesh' in full) else ''
    d['礼盒'] = '✅' if 'gift' in full else ''
    d['brand_type'] = '官方' if brand in official_brands else '第三方'
    d['is_competitor'] = (d['type'] == TARGET_VALUE)
    return d

def cn_title_smoker(row):
    brand = str(gv(row,'品牌') or '')
    t = row.get('type','')
    mat = row.get('material','')
    ch = row.get('充电','')
    chips = row.get('木屑','')
    parts = [f"[{t}]", brand, mat]
    if ch not in ('未标注',''): parts.append(ch)
    if chips not in ('未标注',''): parts.append(chips)
    if row.get('LED')=='✅': parts.append('LED')
    if row.get('安全盖')=='✅': parts.append('安全盖')
    return ' '.join(parts)

def selling_smoker(row):
    full = (str(gv(row,'商品标题') or '') + ' ' + str(gv(row,'产品卖点') or '')).lower()
    pts = []
    for en,cn in {'no butane':'无需丁烷','usb':'USB充电','led':'LED灯','electric':'电动',
                  'rechargeable':'可充电','waterproof':'防水','gift':'礼盒装','cold smoke':'冷烟',
                  'smoke':'烟熏','magnetic':'磁吸盖','fan':'风扇','wood chip':'木屑'}.items():
        if en in full: pts.append(cn)
    m = re.search(r'(\d+)\s*(wood chip|chips|flavor)', full)
    if m: pts.append(f"{m.group(1)}种木屑")
    return '，'.join(pts[:6]) if pts else '—'

SMOKER_HEADERS = [
    "#","图","中文标题","品牌","类型","材质","充电","LED","显示屏","安全盖","风扇",
    "价格$","Prime$","Coupon","评分","评数","上架","ASIN","链接",
    "月销","月销$","月销¥","木屑","冷烟","含喷枪","过滤嘴","礼盒",
    "品牌类型","AC","BSeller","变体","天数","LQS","FBA","运费$","A+","视频","卖点(中文)"
]
SMOKER_ROW = lambda row, idx, asin, is_tgt: [
    idx+1, None, row.get('cn_title',''), gv(row,'品牌'),
    row.get('type',''), row.get('material',''), row.get('充电',''), row.get('LED',''),
    row.get('显示屏',''), row.get('安全盖',''), row.get('风扇',''),
    f"${gv(row,'价格($)'):,.2f}" if gv(row,'价格($)') and not pd.isna(gv(row,'价格($)')) else '',
    f"${gv(row,'Prime价格($)'):,.2f}" if gv(row,'Prime价格($)') and not pd.isna(gv(row,'Prime价格($)')) else '—',
    str(gv(row,'Coupon') or '—'), gv(row,'评分'),
    f"{int(gv(row,'评分数')):,}" if gv(row,'评分数') and not pd.isna(gv(row,'评分数')) else '',
    str(gv(row,'上架时间') or '')[:10], asin,
    gv(row,'商品详情页链接') or f"https://www.amazon.com/dp/{asin}",
    f"{int(gv(row,'月销量')):,}" if gv(row,'月销量') and not pd.isna(gv(row,'月销量')) else '',
    f"${gv(row,'月销售额($)'):,.0f}" if gv(row,'月销售额($)') and not pd.isna(gv(row,'月销售额($)')) else '',
    f"¥{gv(row,'月销售额($)')*EXCHANGE:,.0f}" if gv(row,'月销售额($)') and not pd.isna(gv(row,'月销售额($)')) else '',
    row.get('木屑',''), row.get('冷烟',''), row.get('含喷枪',''), row.get('过滤嘴',''), row.get('礼盒',''),
    row.get('brand_type',''),
    '✅' if str(gv(row,"Amazon's Choice")or'').upper()=='Y' else '',
    '✅' if str(gv(row,'Best Seller标识')or'').upper()=='Y' else '',
    str(gv(row,'变体数') or '1'), str(gv(row,'上架天数') or ''), str(gv(row,'LQS') or ''),
    str(gv(row,'配送方式') or ''),
    f"${gv(row,'FBA($)'):,.2f}" if gv(row,'FBA($)') and not pd.isna(gv(row,'FBA($)')) else '—',
    '✅' if str(gv(row,'A+页面')or'').upper()=='Y' else '',
    '✅' if str(gv(row,'视频介绍')or'').upper()=='Y' else '',
    row.get('卖点中文',''),
]

# ══════════════════════════════════════════════════════════════
# 类目C: 鸡尾酒调酒器 (shaker)
# ══════════════════════════════════════════════════════════════
def classify_shaker(row):
    title = str(gv(row,'商品标题') or '').lower()
    bullets = str(gv(row,'产品卖点') or '').lower()
    params = str(gv(row,'详细参数') or '').lower()
    full = title + ' ' + bullets + ' ' + params
    brand = str(gv(row,'品牌') or '').lower().strip()
    d = {}
    # 类型
    if 'whiskey stone' in full or 'ice cube' in full or 'chilling rock' in full or 'chilling stone' in full:
        d['type'] = '冰石/冰模'
    elif 'muddler' in title or 'mixing spoon' in title or 'bar spoon' in title or 'jigger' in title:
        d['type'] = '单品工具'
    elif 'shaker' in full or 'bartender' in full or 'bar set' in full or 'mixology' in full or 'cocktail kit' in full:
        d['type'] = '摇酒器套装'
    else: d['type'] = '其他'
    # 件数
    m = re.search(r'(\d+)\s*(piece|pc|pcs)', full)
    d['件数'] = f"{m.group(1)}件" if m else '未标注'
    # 材质
    if 'stainless steel' in full: m = '不锈钢'
    elif 'glass' in full: m = '玻璃'
    elif 'wood' in full or 'bamboo' in full: m = '木质'
    elif 'plastic' in full: m = '塑料'
    elif 'copper' in full: m = '铜'
    else: m = '未标注'
    d['material'] = m
    # 颜色
    color_map = [('silver','银色'),('black','黑色'),('gold','金色'),('copper','铜色'),('rose gold','玫瑰金'),('gunmetal','枪灰')]
    d['颜色'] = next((cn for en,cn in color_map if en in full), '未标注')
    # 支架
    if 'stand' in full and 'bamboo' in full: s = '竹支架'
    elif 'stand' in full and 'acrylic' in full: s = '亚克力支架'
    elif 'stand' in full and 'wood' in full: s = '木支架'
    elif 'stand' in full: s = '有支架'
    else: s = '无'
    d['支架'] = s
    # 摇酒器类型
    if 'boston' in full: sh = '波士顿'
    elif 'cobbler' in full: sh = '日式Cobbler'
    elif 'shaker' in full: sh = '普通'
    else: sh = '—'
    d['摇酒器'] = sh
    # 配件
    d['捣棒'] = '✅' if 'muddler' in full else ''
    d['量杯'] = '✅' if 'jigger' in full else ''
    d['过滤器'] = '✅' if 'strainer' in full else ''
    d['配方卡'] = '✅' if ('recipe' in full or 'recipe card' in full) else ''
    d['礼盒'] = '✅' if 'gift' in full else ''
    d['便携包'] = '✅' if ('bag' in full or 'travel' in full) else ''
    d['brand_type'] = '官方' if brand in official_brands else '第三方'
    d['is_competitor'] = (d['type'] == TARGET_VALUE)
    return d

def cn_title_shaker(row):
    brand = str(gv(row,'品牌') or '')
    t = row.get('type','')
    mat = row.get('material','')
    n = row.get('件数','')
    col = row.get('颜色','')
    parts = [f"[{t}]", brand, mat]
    if n not in ('未标注',''): parts.append(n)
    if col not in ('未标注',''): parts.append(col)
    return ' '.join(parts)

def selling_shaker(row):
    full = (str(gv(row,'商品标题') or '') + ' ' + str(gv(row,'产品卖点') or '')).lower()
    pts = []
    for en,cn in {'stainless steel':'不锈钢','dishwasher':'可洗碗机','leak-proof':'防漏',
                  'leak proof':'防漏','rust':'防锈','gift':'礼盒','recipe':'配方卡',
                  'bamboo':'竹支架','18/8':'18/8钢','304':'304钢','boston':'波士顿'}.items():
        if en in full: pts.append(cn)
    m = re.search(r'(\d+)\s*(piece|pc|pcs)', full)
    if m: pts.append(f"{m.group(1)}件套")
    return '，'.join(pts[:6]) if pts else '—'

SHAKER_HEADERS = [
    "#","图","中文标题","品牌","类型","材质","颜色","件数","支架","摇酒器",
    "价格$","Prime$","Coupon","评分","评数","上架","ASIN","链接",
    "月销","月销$","月销¥","捣棒","量杯","过滤器","配方卡","礼盒","便携包",
    "品牌类型","AC","BSeller","变体","天数","LQS","FBA","运费$","A+","视频","卖点(中文)"
]
SHAKER_ROW = lambda row, idx, asin, is_tgt: [
    idx+1, None, row.get('cn_title',''), gv(row,'品牌'),
    row.get('type',''), row.get('material',''), row.get('颜色',''), row.get('件数',''),
    row.get('支架',''), row.get('摇酒器',''),
    f"${gv(row,'价格($)'):,.2f}" if gv(row,'价格($)') and not pd.isna(gv(row,'价格($)')) else '',
    f"${gv(row,'Prime价格($)'):,.2f}" if gv(row,'Prime价格($)') and not pd.isna(gv(row,'Prime价格($)')) else '—',
    str(gv(row,'Coupon') or '—'), gv(row,'评分'),
    f"{int(gv(row,'评分数')):,}" if gv(row,'评分数') and not pd.isna(gv(row,'评分数')) else '',
    str(gv(row,'上架时间') or '')[:10], asin,
    gv(row,'商品详情页链接') or f"https://www.amazon.com/dp/{asin}",
    f"{int(gv(row,'月销量')):,}" if gv(row,'月销量') and not pd.isna(gv(row,'月销量')) else '',
    f"${gv(row,'月销售额($)'):,.0f}" if gv(row,'月销售额($)') and not pd.isna(gv(row,'月销售额($)')) else '',
    f"¥{gv(row,'月销售额($)')*EXCHANGE:,.0f}" if gv(row,'月销售额($)') and not pd.isna(gv(row,'月销售额($)')) else '',
    row.get('捣棒',''), row.get('量杯',''), row.get('过滤器',''), row.get('配方卡',''),
    row.get('礼盒',''), row.get('便携包',''),
    row.get('brand_type',''),
    '✅' if str(gv(row,"Amazon's Choice")or'').upper()=='Y' else '',
    '✅' if str(gv(row,'Best Seller标识')or'').upper()=='Y' else '',
    str(gv(row,'变体数') or '1'), str(gv(row,'上架天数') or ''), str(gv(row,'LQS') or ''),
    str(gv(row,'配送方式') or ''),
    f"${gv(row,'FBA($)'):,.2f}" if gv(row,'FBA($)') and not pd.isna(gv(row,'FBA($)')) else '—',
    '✅' if str(gv(row,'A+页面')or'').upper()=='Y' else '',
    '✅' if str(gv(row,'视频介绍')or'').upper()=='Y' else '',
    row.get('卖点中文',''),
]

# ══════════════════ 类目分发 ══════════════════
DISPATCH = {
    'bands':  (classify_bands,  cn_title_bands,  selling_bands,  BANDS_HEADERS,  BANDS_ROW),
    'smoker': (classify_smoker, cn_title_smoker, selling_smoker, SMOKER_HEADERS, SMOKER_ROW),
    'shaker': (classify_shaker, cn_title_shaker, selling_shaker, SHAKER_HEADERS, SHAKER_ROW),
}
if CATEGORY_TYPE not in DISPATCH:
    print(f"❌ 未知类目类型: {CATEGORY_TYPE}，可选: {list(DISPATCH.keys())}")
    sys.exit(1)

CLASSIFY_FN, CN_TITLE_FN, SELLING_FN, HEADERS, ROW_FN = DISPATCH[CATEGORY_TYPE]

# ══════════════════ 应用分类 ══════════════════
for idx, row in df.iterrows():
    info = CLASSIFY_FN(row)
    for k, v in info.items(): df.at[idx, k] = v
df['cn_title'] = df.apply(CN_TITLE_FN, axis=1)
df['卖点中文'] = df.apply(SELLING_FN, axis=1)

# ══════════════════ 下载缩略图 ══════════════════
img_dir = "/tmp/_bsr_images"
os.makedirs(img_dir, exist_ok=True)
for idx, row in df.iterrows():
    asin = str(gv(row,'ASIN') or '')
    local = os.path.join(img_dir, f"{asin}.jpg")
    if os.path.exists(local): continue
    img_url = str(gv(row,'商品主图') or '')
    if not img_url or img_url == 'nan': continue
    try:
        r = requests.get(img_url, timeout=10, headers={'User-Agent':'Mozilla/5.0'})
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content)); img.thumbnail((55,55), Image.LANCZOS)
            img.save(local, 'JPEG', quality=80)
    except: pass

# ══════════════════ 构建Excel ══════════════════
wb = Workbook(); ws = wb.active; ws.title = "BSR分析"

HDR_FILL = PatternFill("solid","1F4E79"); YEL_FILL = PatternFill("solid","FFFFCC")
RED_FILL = PatternFill("solid","FFC7CE"); BLU_FILL = PatternFill("solid","BDD7EE")
GRY_FILL = PatternFill("solid","F0F0F0"); GRN_BG = PatternFill("solid","E2EFDA")
RED_BG = PatternFill("solid","F2DCDB")
BF9=Font(bold=True,size=9); NF9=Font(size=9)
CEN=Alignment(horizontal="center",wrap_text=True,vertical="center")
WRA=Alignment(wrap_text=True,vertical="top")
BOR=Border(left=Side('thin'),right=Side('thin'),top=Side('thin'),bottom=Side('thin'))

# 计算最后一列字母
from openpyxl.utils import get_column_letter as gcl
LAST_COL = gcl(len(HEADERS))

# R1 Title
ws.merge_cells(f"A1:{LAST_COL}1")
ws["A1"] = f"{CATEGORY_NAME} BSR100 | 1USD={EXCHANGE}CNY ({TODAY}) | 目标:{TARGET_ASIN} | 「—」=不适用"
ws["A1"].font = Font(bold=True,size=13,color="1F4E79"); ws["A1"].fill = GRY_FILL; ws["A1"].alignment = CEN

# R2 Stats
n_comp = int(df['is_competitor'].sum()) if 'is_competitor' in df.columns else 0
tms = int(sum(v for v in df['月销量'] if not pd.isna(v)))
trev = int(sum(v for v in df['月销售额($)'] if not pd.isna(v)))
avg_p = df['价格($)'].mean()
ws.merge_cells(f"A2:{LAST_COL}2")
ws["A2"] = f"{len(df)}产品 | 月销{tms:,} | ${trev/1000:,.0f}K(¥{trev*EXCHANGE/10000:,.0f}万) | 均价${avg_p:.0f} | 竞品{n_comp}个"
ws["A2"].font = Font(bold=True,size=9); ws["A2"].fill = GRY_FILL

# R3 Headers
for j,h in enumerate(HEADERS,1):
    c = ws.cell(row=3,column=j,value=h)
    c.font=Font(bold=True,size=8,color="000000"); c.fill=YEL_FILL; c.alignment=CEN; c.border=BOR

# R4+ Data
for idx,(_,row) in enumerate(df.iterrows()):
    r = 4+idx; asin = str(gv(row,'ASIN') or '')
    is_tgt = (asin == TARGET_ASIN); is_comp = row.get('is_competitor', False)
    vals = ROW_FN(row, idx, asin, is_tgt)
    for j,val in enumerate(vals,1):
        c=ws.cell(row=r,column=j,value=val); c.font=BF9 if is_tgt else NF9; c.alignment=WRA; c.border=BOR
        if is_tgt: c.fill=RED_FILL
        elif is_comp: c.fill=BLU_FILL
    ip=os.path.join(img_dir,f"{asin}.jpg")
    if os.path.exists(ip):
        try: img=XLImage(ip); img.width=53; img.height=53; ws.add_image(img,f"B{r}")
        except: pass
    ws.row_dimensions[r].height=55

# 列宽（自动：A-D窄，标题/链接/卖点宽）
for j in range(1, len(HEADERS)+1):
    col = gcl(j)
    hdr = HEADERS[j-1]
    if hdr in ('#','AC','BSeller','A+','视频','LED','显示屏','安全盖','风扇','冷烟','含喷枪','过滤嘴','捣棒','量杯','过滤器','配方卡','便携包','礼盒'):
        ws.column_dimensions[col].width = 5
    elif hdr in ('图',):
        ws.column_dimensions[col].width = 8
    elif hdr in ('中文标题','卖点(中文)'):
        ws.column_dimensions[col].width = 28
    elif hdr in ('链接',):
        ws.column_dimensions[col].width = 8
    elif hdr in ('材质细分','外观类型','适配设备','扣环','材质','类型','品牌类型','佩戴','防水'):
        ws.column_dimensions[col].width = 18
    elif hdr in ('ASIN',):
        ws.column_dimensions[col].width = 12
    elif hdr in ('价格$','Prime$','月销$','月销¥','运费$'):
        ws.column_dimensions[col].width = 8
    else:
        ws.column_dimensions[col].width = 9

ws.auto_filter.ref = f"A3:{LAST_COL}{3+len(df)}"
ws.freeze_panes = "A4"
ws.row_dimensions[3].height = 30

# ══════════════════ 结论区（按实际数据填入） ══════════════════
r = 4+len(df)+1
ws.merge_cells(f"A{r}:{LAST_COL}{r}")
ws.cell(row=r,column=1,value="═"*20+" 结论分析 "+"═"*20).font = Font(bold=True,size=13,color="1F4E79")
ws.cell(row=r,column=1).fill = GRY_FILL
# 这里按 SKILL.md Step 7 填入 市场结构/演变/竞品对标/切入建议/兼容性Q&A

wb.save(OUTPUT)
print(f"\n✅ Saved: {OUTPUT}")
wb.close()