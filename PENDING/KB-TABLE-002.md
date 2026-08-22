---
id: KB-TABLE-002
title: 单位统一——重量g/kg、容量ml/L/mAh、价格USD
type: rule（规则）
category: source_rules（来源规则）
tags: [单位, 换算, 统一, 重量, 容量, 尺寸, 价格]
roles: [Commander, data-analyst, Data Verifier]
status: pending（待审核）
confidence: A（用户宪法铁律92-110 + category-fields.md）
source: 威猛先生宪法铁律92-110
evidence: 字段库明确规定单位统一
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-TABLE-001, KB-FIELD-005]
---

# 单位统一——重量g/kg、容量ml/L/mAh、价格USD

## 规则结论

所有表格数据的单位必须统一。不同单位必须换算，禁止混用。单位不统一导致排序/对比/统计全部无效。

## 强制统一标准

| 类别 | 统一单位 | 禁止混用 |
|------|---------|---------|
| 重量 | g / kg | lb和kg混用 |
| 容量 | ml / L / mAh | oz和ml混用 |
| 尺寸 | cm / inch | inch和cm混用不换算 |
| 价格 | USD | USD和RMB混用不标注汇率 |
| 销售额 | USD或RMB，必须注明 | 不标注币种 |
| 功率 | W | W和HP混用 |
| 电压 | V | —
| 时间 | 秒/分钟/小时 | 小时和分钟混写 |
| 占比 | % | 小数和%混用 |
| 压力 | PSI/Bar | PSI和Bar混用不换算 |

## 容易踩坑的换算

- lb → kg：×0.4536
- oz → ml：×29.57
- inch → cm：×2.54
- mAh → Wh：mAh × V / 1000（需知道电压）
- 日销量 → 月销量：×30（必须标注"估算"）
- mAh和Wh不能混用不说明

## 错误表现

1. 重量列混用lb和kg（不经换算直接放一起）
2. 尺寸列混用inch和cm
3. 人民币和美元混排不标注汇率
4. mAh和Wh同时出现不说明
5. 日销量和月销量放同一列

## 正确做法

- 原始数据保留一列，换算后加一列
- 例：重量(lb)保留，新增"重量(g)"列 = lb × 453.6
- 标价保留，新增"有效价(Coupon后)"
- 表头标注单位：价格($)、重量(g)、尺寸(cm)

## 适用场景

所有数据表格。

## 禁止再犯

是。

## 来源证据

- 威猛先生宪法铁律92-110
- category-fields.md: "重量统一g/kg，容量统一ml/L/mAh，尺寸统一cm/in，压力统一PSI/Bar，功率统一W，电压统一V"

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |