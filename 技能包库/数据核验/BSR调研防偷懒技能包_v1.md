---
name: bsr-anti-slacking-skillpack
description: BSR调研防偷懒技能包。含十大铁坑速查表、电动分类决策树、Alexa必问清单、空值扫描脚本。每次调研前必读。
version: 1.0.0
category: ecommerce
tags: [防偷懒, BSR, 失败案例, 分类, 空值扫描, Alexa, 竞品核实, 铁律, 电动分类, 字段补齐]
roles: [Commander, Product Analyst, Data Verifier]
created_at: 2026-08-26
updated_at: 2026-08-26
source: 威猛先生BSR调研中累积的失败案例与实践经验
---

# BSR调研防偷懒技能包

> 本文档汇总了所有BSR调研中踩过的坑。每次开始新类目调研前，必须通读本文档。 
> 关联知识库：KB-FAIL-005, KB-FAIL-006, KB-FAIL-007, KB-FAIL-008

---

## 十大铁坑速查表（每次调研前必须过一遍）

| # | 坑 | 错误表现 | 正确做法 |
|---|----|---------|---------|
| 1 | **Automatic ≠ 电动** | 标题含 "Automatic Bead Dispenser" 就归为电动 | 必须有 battery/electric/motor/usb 等**电源证据**，否则问Alexa "is this electric or manual?" |
| 2 | **场景词 ≠ 类型词** | "for cast iron" 当成 "铸铁清洁刷" 分类 | 类型词在标题，场景词在五点。场景词归"使用场景"列 |
| 3 | **light子串误判** | `'light' in text` 匹配到 "lightweight"、"FlexTexture" | 用词边界正则 `\\bled light\\b` 或精确词组，禁止子串匹配 |
| 4 | **分类兜底** | "烧烤刷(通用)" 占38%兜底 | 兜底类必须 < 10%，超过 → 必须拆分物理结构（刷毛/无刷毛/螺旋/尼龙等） |
| 5 | **中文标题留空** | 卖家精灵"标题(翻译)"字段为空就留空 | 必须有 fallback 生成逻辑（品牌+核心功能+材质+规格），100条不允许空白 |
| 6 | **竞品核实缩水** | 6个竞品只核3个就急于建表 | 选定几个必须核几个，缺的标 UNKNOWN_CHECKED，不能假装核了 |
| 7 | **说一套做一套** | 结论写"HAZENS/OXO已移除电动"，但数据没改 | 改结论必须同步改数据，改完立即跑字段校验 |
| 8 | **交付前不自检** | 空值率19%直接发用户 | 保存后立即逐列扫描空值，空值率 > 10% 禁止交付 |
| 9 | **steam≠自带加热** | "蒸汽清洗刷" 独立成类，实际全是无刷毛刷+烤架余热 | 必须查产品是否自带加热元件，不能仅凭 "steam" 关键字分类 |
| 10 | **电动竞品功能参数字段大面积空白** | 电池mAh/防水IP/杆子长度等列全空，只核实了材质和颜色 | 电动类专属字段必须逐ASIN用Alexa核实：电机有刷无刷、RPM、mAh、IP等级、续航分钟数、杆长、充电方式 |

---

## 一、电动/手动分类决策树

```
标题/五点/详细参数 有 battery/electric/motor/usb/mAh/type-c/rechargeable 任一电源词？
    ├─ YES → 归入电动
    └─ NO → 标题含 electric 但修饰的是其他词？
            ├─ YES → "Electric Grill Brush" 但实际是"给电烤盘用的清洁刷"("electric"修饰grill不是brush)→ 手动
            └─ NO → 归入手动
    
**反问检查**：这个产品有没有 电机/电池/充电接口？
- 三个证据都有 → 电动
- 只有"automatic/dispenser/press"没有电源证据 → 手动
- 没有电源证据 → 手动
```

---

## 二、Alexa必问清单

### 电动/带电产品必问
```
"For ASIN [XXXX], what is the max pressure/flow/speed in RPM/PSI? Answer only based on the listing."
"For ASIN [XXXX], is this electric powered, battery powered, or manual? Answer only based on the listing."
"For ASIN [XXXX], is the motor brushed or brushless? Answer only based on the listing."
"For ASIN [XXXX], what is the battery capacity in mAh? Answer only based on the listing."
"For ASIN [XXXX], what IP waterproof rating does it have? Answer only based on the listing."
"For ASIN [XXXX], how long does the battery last per charge? Answer only based on the listing."
"For ASIN [XXXX], what type of charging port does it use (Type-C/Micro USB/Proprietary)? Answer only based on the listing."
```

### 未核实分类必问
```
"For ASIN [XXXX], is this product electric, battery-powered, gas-powered, or manual? Does it have a motor, battery, or engine? Answer only based on the listing."
```

---

## 三、关键字匹配防坑规则

| 关键字 | ❌ 错误匹配 | ✅ 正确匹配 |
|--------|----------|----------|
| `light` | "lightweight", "FlexTexture" | `\\bled light\\b` 精确词边界 |
| `led` | "tangled", "installed", "disabled" | `\\bled\\b` 精确词边界 |
| `ce ` | "piece", "once", "price" | 认证从 Product Overview 字段提取，不全文搜 |
| `automatic` | 直接判断为电动 | 必须有电源证据（electric/battery/motor/USB）配合判断 |
| `electric` | "Electric Grill and Panini Press Brush"→电动 | 看 electric 修饰的是哪个名词：grill (烤盘)→手动刷，tool (工具)→电动 |

---

## 四、竞品时效要求

1. **主要对标必须是近一年内上架的**（从调研日往前推12个月）。
2. **超过一年的只做参考**，最多放1-2个老品牌做价格锚点。
3. 竞品选择时先把前100按上架时间过滤，近一年的高销量优先级最高。

---

## 五、空值扫描模板（每次交付前必跑）

```python
from openpyxl import load_workbook
wb = load_workbook('你的表格.xlsx')
ws = wb.active
total, empty = 0, 0
for ci in range(1, ws.max_column + 1):
    col_empty = sum(1 for r in range(4, 104) if ws.cell(row=r, column=ci).value in (None, ''))
    if col_empty > 10:
        print(f'⚠️ {ws.cell(row=3, column=ci).value}: {col_empty}个空值')
    empty += col_empty; total += 100
rate = empty / total * 100 if total else 0
print(f'空值率: {rate:.1f}%')
print('❌ 禁止交付！' if rate > 10 else '✅ 可交付')
```

---

## 六、确保功能参数字段不空白（特别针对电动/带电产品）

凡是带电的产品，必须输出以下字段，缺的逐个ASIN补查：
- 是否有刷电机/无刷电机
- 转速（RPM）
- 电池容量（mAh）
- 防水等级（IPX4/IP65/IP67/未标）
- 续航时间（分钟）
- 杆子/手柄长度
- 充电方式（Type-C/Micro USB/专用座充/插电）

字段来源优先级：Product Overview > 标题 > 五点 > 图片 > A+ > Alexa > 卖家精灵

---

## 七、禁止事项清单

1. ❌ 禁止不看详情就凭关键词分类
2. ❌ 禁止竞品核实只核实为了"凑数"（核实要是指定参数，不是翻页面）
3. ❌ 禁止结论改了但数据没改（说一套做一套）
4. ❌ 禁止文件没有空值扫描就直接发送
5. ❌ 禁止套用老产品的数据给新竞品
6. ❌ 禁止随便写"未标注"而不去核实
7. ❌ 禁止写笼统词（电池、电机、防水）代替具体数值
8. ❌ 禁止超过一年的产品作为主要竞品
9. ❌ 禁止`'light' in text`这种子串匹配
10. ❌ 禁止标题含`steam`就当成"蒸汽类目"

---

## 八、关联失败案例

| ID | 教训 | 适用场景 |
|----|------|---------|
| KB-FAIL-005 | automatic/dispenser/press≠电动 | 电动工具/钻石画/带自动字样的产品 |
| KB-FAIL-006 | 中文标题30条空白/场景词误判/light子串 | BSR通用 |
| KB-FAIL-007 | 电压兜底/竞品不全/缺图/无交叉验证 | 电动工具/String Trimmers |
| KB-FAIL-008 | 空值扫描+分类误判未自检 | BSR通用 |

---

## 九、技能包集成

- 本技能包是 `product-analysis-page2` 的强化防偷懒版
- 每次BSR第二页任务开始前，先通读「十大铁坑」
- 和 SYS-008（证据门禁制）互补——证据门禁制规定了数据核实流程，本技能包规定了常犯错误的预防