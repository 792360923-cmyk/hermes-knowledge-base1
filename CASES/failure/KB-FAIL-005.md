---
id: KB-FAIL-005
title: automatic/dispenser/press不能直接判定为电动——电动/手动/机械按压必须逐ASIN问Alexa核实
type: case（案例）
category: classification_rules（分类规则）
tags: [失败案例, 分类错误, 电动, 手动, 机械按压, automatic, dispenser, Alexa核实, 钻石画工具, 吸钻笔]
roles: [Commander, Product Analyst, Data Verifier]
status: pending（待审核）
confidence: A（实际发生+用户亲自纠正）
source: Diamond Painting BSR调研返工记录
evidence: 威猛先生2026-08-24亲自纠正：B0HC72TVK4等6个"Automatic Bead Dispenser"被误判为电动，Alexa核实为机械手动按压
created_at: 2026-08-24
updated_at: 2026-08-24
reviewed_by: 待审核
related: [KB-CLASSIFY-001, KB-FIELD-001, KB-FIELD-002]
---

# automatic/dispenser/press 不能直接判定为电动

## 错误表现

B0HC72TVK4（Ironbark Relief "Bead Blitz Automatic Diamond Painting Bead Dispenser"）被错误分类为"电动吸钻笔"。

实际 Alexa 核实：**机械手动按压款**，无电机、无电池、无USB充电，靠手按压出钻。

同类误判 ASIN（6个，全部是"Automatic Bead Dispenser"营销词）：
- B0HC72TVK4（Ironbark Relief Bead Blitz）
- B0HCC15YS3（Generic）
- B0HBQJNVTN（Generic）
- B0HC97G5C3（Generic）
- B0HCPDTBWM（ScontLuy）
- B0HBQ8ZNHJ（Generic）

这6个产品标题都含"Automatic"+"Bead Dispenser"，但标题和五点里完全没有 battery/electric/motor/usb/rechargeable/vacuum/suction 任何电源证据，却凭"automatic/dispenser"营销词归为电动。

## 错误原因

1. 用标题关键词"automatic/dispenser"推断产品工作方式，没核实是否有电机/电池/充电。
2. "Automatic"是营销词，实际是"机械自动进给"（手按出钻），不等于电动。
3. 未逐个 ASIN 问 Alexa 核实真实工作方式。

## 正确做法

涉及电动/手动/机械按压/整机/配件/耗材/套装的主分类判断，必须逐 ASIN 核实：

1. **页面证据**：Product Overview / Technical Details 是否有 Power Source（Battery Powered / USB / Corded Electric）
2. **标题+五点证据**：是否有 electric / battery / motor / usb rechargeable / type-c / vacuum / suction / mAh / cable
3. **Alexa 必问**：
   "For ASIN [ASIN], is this product electric powered, battery powered, motorized, or a manual/mechanical press operated by hand? Does it have a motor, battery, or USB charging? Please answer only based on the listing."
4. **分类规则**：
   - 有 battery/electric/motor/USB rechargeable 明确证据 → 电动
   - Alexa 明确 manual/mechanical/hand press/non-electric → 手动或机械手动按压
   - 只有 automatic/dispenser/press 词，无电源证据 → 不能归电动，必须核实或待核实
   - Alexa 无法确认 → 待核实

## 后果

- 产品主分类错误率 38%（16个吸钻笔中6个误判）
- 电动款数量、均价、市场占比统计全错
- 结论"做电动笔"的依据失真——实际6个是低质机械按压款

## 适用场景

Amazon BSR 产品分类、钻石画工具、点钻笔、吸钻笔、手工工具、带电/非带电产品、主产品/配件混杂类目、含 automatic/dispenser/press 字样的产品。

## 教训

"automatic/dispenser/press"是营销词不是电源证据。没有 battery/electric/motor/USB 证据，禁止归为电动。电动/手动/机械按压必须逐 ASIN 问 Alexa，答不出就"待核实"。

## 禁止再犯

是。

## 来源证据

- 威猛先生2026-08-24亲自纠正：B0HC72TVK4 等6个"Automatic Bead Dispenser"误判为电动，Alexa核实为机械手动按压（无电机无电池无USB），分类错误率38%

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-24 | 初始创建（失败案例） | Commander |
