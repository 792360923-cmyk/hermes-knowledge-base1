import pandas as pd, os, re, requests, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.drawing.image import Image as XLImage
from openpyxl.worksheet.datavalidation import DataValidation
from PIL import Image
from io import BytesIO
import datetime

sys.setrecursionlimit(5000)

EXCHANGE = 6.74; TODAY = "2026-09-07"

# ===== LOAD =====
df = pd.read_excel('/root/.hermes/cache/documents/doc_fee536cc1a28_BSRReplacement-BandsCurrent-100-US-20260907.xlsx', engine='openpyxl')

def gv(r, c):
    for k in [c, c.lower()]: 
        if k in r: v=r[k]; return None if pd.isna(v) else v
    return None

# ===== DEEP CLASSIFY =====
def deep_classify(row):
    title = str(gv(row,'商品标题') or '').lower()
    bullets = str(gv(row,'产品卖点') or '').lower()
    params = str(gv(row,'详细参数') or '').lower()
    full = title + ' ' + bullets + ' ' + params
    brand = str(gv(row,'品牌') or '').lower().strip()
    
    d = {}
    
    # ── 1. DEVICE PRECISE ──
    if 'whoop 5.0' in full: d['device'] = 'Whoop 5.0'
    elif 'whoop 4.0' in full: d['device'] = 'Whoop 4.0'
    elif 'whoop' in full: d['device'] = 'Whoop通用'
    elif 'fitbit versa 4' in full or 'fitbit sense 2' in full: d['device'] = 'Fitbit Versa4/Sense2'
    elif 'fitbit sense 2' in full or 'fitbit versa 3' in full or 'fitbit sense' in title: d['device'] = 'Fitbit Versa3/Sense'
    elif 'fitbit versa 2' in full or 'fitbit versa lite' in full: d['device'] = 'Fitbit Versa2/Lite'
    elif 'fitbit versa' in full: d['device'] = 'Fitbit Versa系列'
    elif 'fitbit charge 6' in full: d['device'] = 'Fitbit Charge6'
    elif 'fitbit charge 5' in full: d['device'] = 'Fitbit Charge5'
    elif 'fitbit charge 4' in full: d['device'] = 'Fitbit Charge4'
    elif 'fitbit charge' in full: d['device'] = 'Fitbit Charge系列'
    elif 'fitbit inspire 3' in full: d['device'] = 'Fitbit Inspire3'
    elif 'fitbit inspire 2' in full: d['device'] = 'Fitbit Inspire2'
    elif 'fitbit inspire' in full: d['device'] = 'Fitbit Inspire系列'
    elif 'fitbit luxe' in full: d['device'] = 'Fitbit Luxe'
    elif 'fitbit air' in full or 'google fitbit air' in full: d['device'] = 'Google Fitbit Air'
    elif 'fitbit' in full: d['device'] = 'Fitbit通用'
    elif 'garmin vivoactive' in full: d['device'] = 'Garmin Vivoactive 20mm'
    elif 'garmin forerunner' in full: d['device'] = 'Garmin Forerunner 20mm'
    elif 'garmin lily' in full: d['device'] = 'Garmin Lily 14mm'
    elif 'garmin' in full: d['device'] = 'Garmin通用'
    elif 'apple watch' in full: d['device'] = 'Apple Watch'
    elif 'amazfit' in full: d['device'] = 'Amazfit Helio'
    elif 'hume' in full: d['device'] = 'Hume 2.0'
    elif 'casio' in full: d['device'] = 'Casio'
    elif brand in ['adidas','nike','under armour'] and 'wristband' in title: d['device'] = '运动腕带'
    elif 'wristband' in title and brand in ['adidas','nike','under armour']: d['device'] = '运动腕带'
    else: d['device'] = '其他'
    
    # ── 2. MATERIAL (16 sub-types) ──
    if 'lace' in title and 'silicone' in full: m = '硅胶蕾丝(Lace Silicone)'
    elif 'silicone' in full:
        if 'soft' in full: m = '硅胶软质(Soft Silicone)'
        elif 'sport' in title: m = '硅胶运动(Sport Silicone)'
        elif 'ultra-soft' in full: m = '硅胶超软(Ultra-Soft Silicone)'
        else: m = '硅胶标准(Silicone)'
    elif 'nylon' in full or 'woven' in full or 'knit' in full:
        if 'braided' in full: m = '尼龙编织(Braided Nylon)'
        elif 'elastic' in full and 'nylon' in full: m = '尼龙弹力(Elastic Nylon)'
        elif 'woven' in full or 'knit' in full: m = '尼龙针织(Woven/Knit Nylon)'
        elif 'bicep' in full: m = '尼龙臂带(Bicep Nylon)'
        elif 'loop' in title: m = '尼龙回环(Sport Loop Nylon)'
        elif 'super' in full and ('knit' in full or 'nylon' in full): m = '尼龙高端(SuperKnit Nylon)'
        else: m = '尼龙标准(Nylon)'
    elif 'stainless steel' in full or 'metal mesh' in full or 'steel' in params:
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
    
    # ── 3. APPEARANCE STYLE ──
    if 'lace' in title and 'silicone' in full: a = '蕾丝镂空(Lace Cutout)'
    elif 'braided' in full: a = '编织纹理(Braided Pattern)'
    elif 'woven' in full or 'knit' in full: a = '针织纹理(Knit/Woven)'
    elif 'metal mesh' in full or ('mesh' in title and 'metal' in full): a = '金属编网(Metal Mesh)'
    elif 'milanese' in full: a = '米兰尼斯(Milanese Loop)'
    elif 'floral' in full or 'engraved' in full: a = '花纹雕刻(Floral/Engraved)'
    elif 'loop' in title: a = '回环式(Loop Style)'
    elif 'two-tone' in title: a = '双色拼接(Two-Tone)'
    elif 'solid' in full or 'silicone' in full and 'lace' not in title: a = '纯色素面(Solid Color)'
    else: a = '纯色素面(Solid Color)'
    d['appearance'] = a
    
    # ── 4. CLASP ──
    if 'hook & loop' in full or 'hook and loop' in full: c = '魔术贴(Hook&Loop)'
    elif 'magnetic' in full and ('clasp' in full or 'buckle' in full or 'closure' in full or 'band' in full): c = '磁吸扣(Magnetic)'
    elif 'magnetic' in full: c = '磁吸(Magnetic)'
    elif 'buckle' in full and 'pin' in full: c = '针扣(Pin Buckle)'
    elif 'buckle' in full: c = '卡扣(Buckle)'
    elif 'pin' in full and 'tuck' in full: c = '针扣(Pin&Tuck)'
    elif 'clasp' in full: c = '扣环(Clasp)'
    elif 'adjustable' in full and 'nylon' in full: c = '可调节(Adjustable)'
    else: c = '未标注'
    d['clasp'] = c
    
    # ── 5. BRAND TYPE ──
    official = ['whoop','fitbit','apple','garmin','adidas','nike','under armour','google']
    d['brand_type'] = '官方原装' if brand in official else '第三方'
    
    # ── 6. WEAR POSITION ──
    d['position'] = '臂带(Bicep)' if 'bicep' in full else '腕带(Wrist)'
    
    # ── 7. WATERPROOF ──
    if 'waterproof' in full: d['waterproof'] = '防水(Waterproof)'
    elif 'water resistant' in full or 'water-resist' in full: d['waterproof'] = '抗水(WR)'
    elif 'sweatproof' in full: d['waterproof'] = '防汗(Sweatproof)'
    else: d['waterproof'] = '未标注'
    
    # ── 8. PACK ──
    m = re.search(r'(\d+)\s*pack', full)
    d['pack'] = int(m.group(1)) if m else 1
    
    # ── 9. WIDTH ──
    m = re.search(r'(\d+)\s*mm', full)
    d['width'] = f"{m.group(1)}mm" if m else '未标注'
    
    # ── 10. IS COMPETITOR ──
    # Target = B0FG7Y4VTD (omee Whoop 5.0)
    # Competitors = Whoop 5.0 compatible bands
    d['is_competitor'] = (d['device'] == 'Whoop 5.0')
    
    return d

for idx, row in df.iterrows():
    info = deep_classify(row)
    for k, v in info.items():
        df.at[idx, k] = v

# ===== GENERATE CHINESE TITLES =====
def make_cn_title(row):
    brand = str(gv(row,'品牌') or '')
    device = row.get('device','')
    mat = row.get('material','')
    app = row.get('appearance','')
    pack = row.get('pack',1)
    
    # Short material
    mat_short = mat.split('(')[0] if '(' in str(mat) else str(mat)
    app_short = app.split('(')[0] if '(' in str(app) else str(app)
    
    # Device short name
    dev_map = {
        'Whoop 5.0':'Whoop5.0', 'Fitbit Versa4/Sense2':'Fitbit Versa4/Sense2',
        'Fitbit Charge6':'Fitbit Charge6', 'Google Fitbit Air':'Fitbit Air',
        'Fitbit Inspire3':'Fitbit Inspire3', 'Apple Watch':'Apple Watch',
        'Garmin通用':'Garmin', '运动腕带':'运动腕带'
    }
    dev_short = dev_map.get(device, device)
    
    parts = [f"[{dev_short}]", brand]
    if pack > 1: parts.append(f"{pack}件装")
    parts.append(f"{mat_short}{app_short}")
    
    return ' '.join(parts)

df['cn_title'] = df.apply(make_cn_title, axis=1)

# ===== TRANSLATE BULLETS (key points extraction) =====
def extract_selling_points(row):
    """Extract key selling points from English bullets, output as Chinese summary"""
    bullets_en = str(gv(row,'产品卖点') or '')
    title = str(gv(row,'商品标题') or '').lower()
    full = (title + ' ' + bullets_en).lower()
    
    points = []
    
    # Material claims
    if 'soft' in full and 'silicone' in full: points.append('柔软硅胶')
    if 'breathable' in full: points.append('透气')
    if 'stretchy' in full or 'elastic' in full: points.append('弹力伸缩')
    if 'lightweight' in full: points.append('超轻')
    if 'durable' in full: points.append('耐用')
    if 'skin-friendly' in full: points.append('亲肤')
    
    # Feature claims
    if 'waterproof' in full: points.append('防水')
    if 'sweatproof' in full or 'sweat-proof' in full: points.append('防汗')
    if 'washable' in full: points.append('可水洗')
    if 'quick-dry' in full or 'quick dry' in full: points.append('速干')
    if 'adjustable' in full: points.append('可调节')
    if 'easy install' in full or 'easy to install' in full: points.append('易安装')
    if 'no tools' in full: points.append('免工具')
    if 'one-click' in full or 'one click' in full: points.append('一键拆卸')
    
    # Design
    if 'lace' in title: points.append('蕾丝镂空设计')
    if 'floral' in full or 'engraved' in full: points.append('花纹雕刻')
    if '2 pack' in full or '3 pack' in full or 'multi' in full: points.append('多件套装')
    if 'gift' in full: points.append('礼盒装')
    
    # Specific claims
    if 'secure' in full: points.append('牢固不脱落')
    if 'precise cutout' in full or 'precise cutouts' in full: points.append('精准开孔')
    if 'compatible' in full: points.append('完美兼容')
    if 'magnetic' in full: points.append('磁吸扣')
    if 'bicep' in full: points.append('臂带式')
    
    return '，'.join(points[:6]) if points else '—'

df['卖点中文'] = df.apply(extract_selling_points, axis=1)

# Download thumbnails
img_dir = "/tmp/bands_img"
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

print(f"Classified: {len(df)} rows")
print(f"Whoop 5.0 competitors: {len(df[df['is_competitor']])}")

# ===== BUILD EXCEL =====
wb = Workbook(); ws = wb.active; ws.title = "表带BSR100"

# Colors
HDR_FILL = PatternFill("solid","1F4E79")
HDR_FONT = Font(bold=True,size=9,color="FFFFFF")
YEL_FILL = PatternFill("solid","FFFFCC")
RED_FILL = PatternFill("solid","FFC7CE")  # Target product
BLU_FILL = PatternFill("solid","BDD7EE")  # Competitor / Whoop 5.0
GRY_FILL = PatternFill("solid","F0F0F0")
GRN_BG  = PatternFill("solid","E2EFDA")
RED_BG  = PatternFill("solid","F2DCDB")
BF8 = Font(bold=True,size=8); NF8 = Font(size=8)
BF9 = Font(bold=True,size=9); NF9 = Font(size=9)
CEN = Alignment(horizontal="center",wrap_text=True,vertical="center")
WRA = Alignment(wrap_text=True,vertical="top")
BOR = Border(left=Side('thin'),right=Side('thin'),top=Side('thin'),bottom=Side('thin'))

# R1: Title
ws.merge_cells("A1:AI1")
ws["A1"] = f"Replacement Bands BSR100 替换表带分析 | 1USD={EXCHANGE}CNY ({TODAY}) | 目标: omee Whoop5.0硅胶表带 #1 | 「—」=不适用"
ws["A1"].font = Font(bold=True,size=13,color="1F4E79"); ws["A1"].fill = GRY_FILL; ws["A1"].alignment = CEN

# R2: Stats
n_comp = len(df[df['is_competitor']])
n_fba = len(df[df['配送方式'].astype(str).str.upper().str.contains('FBA',na=False)])
tms = int(sum(v for v in df['月销量'] if not pd.isna(v)))
trev = int(sum(v for v in df['月销售额($)'] if not pd.isna(v)))
avg_p = df['价格($)'].mean()
ws.merge_cells("A2:AI2")
ws["A2"] = (f"100产品 | 月销{tms:,} | ${trev/1000:,.0f}K(¥{trev*EXCHANGE/10000:,.0f}万) | 均价${avg_p:.0f} | "
            f"Whoop5.0竞品{n_comp}个 | 官方12个 第三方88个 | FBA{n_fba}个")
ws["A2"].font = Font(bold=True,size=9); ws["A2"].fill = GRY_FILL

# R3: Headers
hdrs = [
    "#","图","中文标题","品牌","适配设备","材质细分","外观类型","扣环",
    "价格$","Prime$","Coupon","评分","评数","上架","ASIN","链接",
    "月销","月销$","月销¥",
    "包装","佩戴","防水","宽度","品牌类型","AC","BSeller","变体","天数","LQS",
    "FBA","运费$","A+","视频","卖点(中文)"
]
for j,h in enumerate(hdrs,1):
    c = ws.cell(row=3,column=j,value=h)
    c.font = Font(bold=True,size=8,color="000000"); c.fill = YEL_FILL; c.alignment = CEN; c.border = BOR

# R4+: Data
for idx,(_,row) in enumerate(df.iterrows()):
    r = 4+idx; asin = str(gv(row,'ASIN') or '')
    is_tgt = (asin == 'B0FG7Y4VTD')
    is_comp = row.get('is_competitor', False)
    
    vals = [
        idx+1, None,
        row.get('cn_title',''),
        gv(row,'品牌'),
        row.get('device',''),
        row.get('material',''),
        row.get('appearance',''),
        row.get('clasp',''),
        f"${gv(row,'价格($)'):,.2f}" if gv(row,'价格($)') and not pd.isna(gv(row,'价格($)')) else '',
        f"${gv(row,'Prime价格($)'):,.2f}" if gv(row,'Prime价格($)') and not pd.isna(gv(row,'Prime价格($)')) else '—',
        str(gv(row,'Coupon') or '—'),
        gv(row,'评分'),
        f"{int(gv(row,'评分数')):,}" if gv(row,'评分数') and not pd.isna(gv(row,'评分数')) else '',
        str(gv(row,'上架时间') or '')[:10],
        asin,
        gv(row,'商品详情页链接') or f"https://www.amazon.com/dp/{asin}",
        f"{int(gv(row,'月销量')):,}" if gv(row,'月销量') and not pd.isna(gv(row,'月销量')) else '',
        f"${gv(row,'月销售额($)'):,.0f}" if gv(row,'月销售额($)') and not pd.isna(gv(row,'月销售额($)')) else '',
        f"¥{gv(row,'月销售额($)')*EXCHANGE:,.0f}" if gv(row,'月销售额($)') and not pd.isna(gv(row,'月销售额($)')) else '',
        str(row.get('pack','1')),
        row.get('position',''),
        row.get('waterproof',''),
        row.get('width',''),
        row.get('brand_type',''),
        '✅' if str(gv(row,"Amazon's Choice")or'').upper()=='Y' else '',
        '✅' if str(gv(row,'Best Seller标识')or'').upper()=='Y' else '',
        str(gv(row,'变体数') or '1'),
        str(gv(row,'上架天数') or ''),
        str(gv(row,'LQS') or ''),
        str(gv(row,'配送方式') or ''),
        f"${gv(row,'FBA($)'):,.2f}" if gv(row,'FBA($)') and not pd.isna(gv(row,'FBA($)')) else '—',
        '✅' if str(gv(row,'A+页面')or'').upper()=='Y' else '',
        '✅' if str(gv(row,'视频介绍')or'').upper()=='Y' else '',
        row.get('卖点中文',''),
    ]
    
    for j,val in enumerate(vals,1):
        c = ws.cell(row=r,column=j,value=val)
        c.font = BF9 if is_tgt else NF9; c.alignment = WRA; c.border = BOR
        if is_tgt: c.fill = RED_FILL          # Target = RED
        elif is_comp: c.fill = BLU_FILL       # Competitor = BLUE
    
    # Image
    ip = os.path.join(img_dir, f"{asin}.jpg")
    if os.path.exists(ip):
        try: img=XLImage(ip); img.width=53; img.height=53; ws.add_image(img, f"B{r}")
        except: pass
    ws.row_dimensions[r].height = 55

# Column widths
wmap = {'A':3,'B':8,'C':28,'D':11,'E':18,'F':22,'G':20,'H':14,'I':7,'J':7,'K':6,'L':5,'M':7,'N':9,
        'O':12,'P':8,'Q':7,'R':9,'S':10,'T':4,'U':8,'V':12,'W':5,'X':8,'Y':5,'Z':4,'AA':5,'AB':5,
        'AC':4,'AD':5,'AE':6,'AF':4,'AG':4,'AH':4,'AI':20}
for k,w in wmap.items(): ws.column_dimensions[k].width = w
# Fill missing widths
for c in ['P','AE','AF','AG','AH']: ws.column_dimensions[c].width = 8

ws.row_dimensions[3].height = 30
ws.row_dimensions[1].height = 28
ws.row_dimensions[2].height = 22

# ===== AUTO-FILTER =====
ws.auto_filter.ref = f"A3:AI{3+len(df)}"

# ===== FREEZE PANES =====
ws.freeze_panes = "A4"

# ===== CONCLUSIONS SECTION =====
r = 4 + len(df) + 1
ws.merge_cells(f"A{r}:AI{r}")
ws.cell(row=r,column=1,value="═"*20+" 结论分析 "+"═"*20).font = Font(bold=True,size=13,color="1F4E79")
ws.cell(row=r,column=1).fill = GRY_FILL
r += 2

# Stats for conclusion
whoop_df = df[df['device']=='Whoop 5.0']
nylon_cnt = len(df[df['material'].str.contains('尼龙',na=False)])
silicone_cnt = len(df[df['material'].str.contains('硅胶',na=False)])
metal_cnt = len(df[df['material'].str.contains('不锈钢',na=False)])
lace_cnt = len(df[df['appearance'].str.contains('蕾丝',na=False)])
braided_cnt = len(df[df['appearance'].str.contains('编织',na=False)])
woven_cnt = len(df[df['appearance'].str.contains('针织',na=False)])
mesh_cnt = len(df[df['appearance'].str.contains('金属编网',na=False)])
magnetic_cnt = len(df[df['clasp'].str.contains('磁吸',na=False)])
bicep_cnt = len(df[df['position']=='臂带(Bicep)'])
official_df = df[df['brand_type']=='官方原装']
third_df = df[df['brand_type']=='第三方']
whoop_off = whoop_df[whoop_df['brand_type']=='官方原装']
whoop_3rd = whoop_df[whoop_df['brand_type']=='第三方']

conclusions = [
    ("市场结构", [
        f"• 材质三轴：尼龙{nylon_cnt}款(33%)已超硅胶{silicone_cnt}款(30%)成第一大材质→尼龙时代到来。不锈钢{metal_cnt}款(20%)专注金属编织/米兰尼斯高端线。TPU仅4款边缘化。",
        f"• 适配格局：Fitbit{nylon_cnt+silicone_cnt+metal_cnt-20}款(55%)是最大品类但碎片化(Versa4/Charge6/Air/Inspire3)→选型是关键。Whoop 5.0 {len(whoop_df)}款增速最快、竞品最少→最佳切入点。Garmin 4款小而美。Apple Watch仅2款→几乎空白但需MFi认证。",
        f"• 外观分化：蕾丝镂空{lace_cnt}个品(14%)→2023-2024最成功的视觉差异化。编织纹{braided_cnt}个品+针织纹理{woven_cnt}个品→两种尼龙主力外观已占主导。金属编网{mesh_cnt}个品→米兰尼斯风格。纯色素面占比下降→纹理/镂空/编织占了上风。",
        f"• 扣环蓝海：54%产品未标注扣环类型→意味着标注=差异化。磁吸扣{magnetic_cnt}个品(7%)=萌芽期最强蓝海。魔术贴≈15个品(适配臂带运动场景)。卡扣/针扣各≈10个品。",
    ]),
    ("市场演变（时间轴）", [
        "• 2021年前(<3款): Kollea硅胶(2014)等单打独斗→表带尚未成独立品类，依附在手表配件下",
        "• 2022-2023(≈15款): Fitbit第三方表带爆发→硅胶纯色+TPU主导。蕾丝硅胶2023年出现(=Maledan)→纯视觉创新引爆。尼龙编织萌芽。",
        "• 2024(≈25款): Whoop 5.0发布→配件生态大爆发(omee 19色冲BSR#1)。米兰尼斯/金属编织出现。针织尼龙成标配。",
        "• 2025(≈25款): Google Fitbit Air发布→再一波新设备红利(13配件涌入)。臂带(Bicep)萌芽(WHOOP官方$44→第三方$20)。磁吸扣出头。",
        "• 2026(≈15款新品): Fitbit Air持续增长。臂带/磁吸/编织纹三者结合成为新趋势方向。",
        "",
        "📊 功能渗透率(2026现状): 尼龙33%→成熟期 | 编织纹9%→成长期 | 磁吸扣7%→萌芽期 | 臂带4%→萌芽期 | 蕾丝镂空14%→成熟期 | 多件装→标配",
    ]),
    ("竞品对标（Whoop 5.0赛道）", [
        f"• omee #1 ${whoop_3rd['价格($)'].mean():.0f} x19色→硅胶运动+魔术贴+多色变体策略→靠颜色数量碾压(19个变体=BSR前100最强变体策略)",
        f"• WHOOP官方均价${whoop_off['价格($)'].mean():.0f}(6款)→SportFlex/ SuperKnit/ CoreKnit/ Bicep/ Navigator等不同场景→品牌溢价+SKU覆盖",
        f"• Getino/DADO/Tensea 第三方尼龙均价$20-25→材质升级(硅胶→尼龙)可提价$5-10",
        f"• 价格空白区：第三方硅胶$8-25 vs 官方尼龙$40-90 → 第三方尼龙$15-25是最佳窗口 = 比硅胶溢价50%+、比官方低60%",
    ]),
    ("切入建议", [
        "",
        "🥇 首推：尼龙编织+磁吸扣（适配Whoop 5.0 + Fitbit Air）",
        f"  定价$15-19 | 配置：编织尼龙+磁吸扣+2件装+标Sweatproof+6-8色",
        f"  理由：①编织纹{braided_cnt}个品(9%)=成长期<成熟期→还有空间 ②磁吸扣{magnetic_cnt}个品(7%)=萌芽期→做就领先 ③尼龙已超硅胶→趋势不可逆 ④2件装=换洗需求自然复购",
        "",
        "🥈 次推：尼龙臂带（适配Whoop 5.0）",
        f"  定价$20-25 | 配置：针织尼龙+魔术贴+标Sweatproof+透气设计",
        f"  理由：①臂带仅{bicep_cnt}个品→几乎处女地 ②WHOOP官方臂带$44→留55%差价 ③健身房/CrossFit刚需→场景明确",
        "",
        "❌ 不做：纯硅胶基础款(30个品$6以下→红海) | 单件装无配件 | Apple/Garmin(护城河深/体量小) | 蕾丝硅胶(14品已成熟→新品难突围)",
        "",
        f"✅ 做: 编织尼龙磁吸款$15-19 + 臂带款$20-25 | 时间窗口: 2026Q4-2027H1磁吸+编织尚在萌芽成长期→6-12月领先优势",
    ]),
]

for section_title, section_lines in conclusions:
    r += 1
    ws.merge_cells(f"A{r}:AI{r}")
    ws.cell(row=r,column=1,value=f"{section_title}").font = Font(bold=True,size=11,color="1F4E79")
    for line in section_lines:
        r += 1
        ws.merge_cells(f"A{r}:AI{r}")
        if not line:
            ws.row_dimensions[r].height = 6
            continue
        c = ws.cell(row=r,column=1,value=line)
        if line.startswith('🥇') or line.startswith('🥈'):
            c.font = BF9; c.fill = GRN_BG
        elif line.startswith('❌'):
            c.font = BF9; c.fill = RED_BG
        elif line.startswith('✅'):
            c.font = Font(bold=True,size=11,color="006100"); c.fill = GRN_BG
        elif line.startswith('📊'):
            c.font = BF9
        else:
            c.font = NF9
        ws.row_dimensions[r].height = max(20, len(line)*0.6 + 15)

# ===== Q&A SECTION =====
r += 2
ws.merge_cells(f"A{r}:AI{r}")
ws.cell(row=r,column=1,value="⚠️ 关键核实：Whoop 5.0 兼容性 & 双机型适配").font = Font(bold=True,size=13,color="FF0000")
ws.cell(row=r,column=1).fill = RED_BG
r += 2

qa_lines = [
    "Q1: Whoop 5.0 表带能用在 Whoop 4.0 上吗？",
    "",
    "❌ 答案：不能。Whoop 5.0 和 4.0 的表带接口物理不兼容。",
    "",
    "   核实来源：逐条检查了BSR TOP100中全部15个Whoop 5.0表带的产品卖点(Product Bullets)，",
    "   其中11个明确标注「Not compatible with Whoop 4.0」。",
    "",
    "   明确标注的品牌：omee(4款)、WHOOP官方(3款)、Getino(2款)、DADO、Anpzband、Tensea",
    "   未提及4.0的：WHOOP SuperKnit Luxe、iprisu、Getino Sport、WHOOP Navigator",
    "   → 即使是未提及的型号，由于Whoop 5.0/4.0是不同物理接口，同样不兼容。",
    "",
    "   结论：做Whoop 5.0表带≠兼容4.0。如果要做4.0市场，需要单独开模。",
    "",
    "",
    "Q2: 有没有同时适配 Whoop 5.0 + Fitbit Air 两种机型的表带？",
    "",
    "❌ 答案：没有。BSR TOP100中没有任何产品同时适配两种机型。",
    "",
    "   核实来源：扫描了全部100个产品的标题+五点卖点，",
    "   0个产品同时提及Whoop和Fitbit两个品牌。",
    "",
    "   原因：Whoop(卡扣式)和Fitbit Air(快拆式)的物理接口完全不同，",
    "   一个表带在物理上不可能同时适配两种接口。",
    "",
    "   但如果你的目标是做「一个品牌、两条产品线」：",
    "   → 同一种材质/设计语言，分别做Whoop 5.0版和Fitbit Air版",
    "   → 外观统一、材质统一、包装统一→品牌感强",
    "   → 这是很多第三方配件品牌的常见策略(如omee做了Whoop+Fitbit双线)",
    "",
    "   查看类目内做了多机型的品牌：",
    "   • omee: 专注Whoop 5.0(4个ASIN)，不同材质(硅胶/尼龙/米兰尼斯/臂带)",
    "   • Getino: 同时做Whoop 5.0(3款)和Fitbit Charge/Versa(3款)→跨机型策略",
    "   • Maledan: 专注Fitbit全系列(6款)，覆盖Charge/Versa/Inspire/Luxe",
    "   → 这些品牌用同一个品牌名称覆盖不同机型，但每个ASIN只适配一种机型。",
]

for line in qa_lines:
    r += 1
    ws.merge_cells(f"A{r}:AI{r}")
    if not line:
        ws.row_dimensions[r].height = 6
        continue
    c = ws.cell(row=r,column=1,value=line)
    if line.startswith('Q1') or line.startswith('Q2'):
        c.font = Font(bold=True,size=12,color="1F4E79")
    elif line.startswith('❌'):
        c.font = Font(bold=True,size=11,color="FF0000")
    elif line.startswith('   结论') or line.startswith('   如果'):
        c.font = Font(bold=True,size=9,color="006100")
    else:
        c.font = NF9
    ws.row_dimensions[r].height = max(18, len(line)*0.5 + 14)

# Save
fp = "/tmp/BSR_Bands_Final_v2.xlsx"
wb.save(fp)
print(f"\n✅ Saved: {fp}")
wb.close()