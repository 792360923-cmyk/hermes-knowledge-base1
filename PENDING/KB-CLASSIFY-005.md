---
id: KB-CLASSIFY-005
title: 图片与标题冲突——优先信图片，标记待核实
type: rule（规则）
category: classification_rules（分类规则）
tags: [图片, 标题, 冲突, 待核实, 来源判断]
roles: [Commander, Product Analyst, Data Verifier]
status: pending（待审核）
confidence: A（宪法铁律+字段库校验规则）
source: 威猛先生宪法铁律49 + category-fields.md校验规则
evidence: 字段库v3.0校验规则：图片和标题冲突时标记待核实，优先信图片
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-CLASSIFY-001, KB-ANTI-FAKE-001, KB-SOURCE-001]
---

# 图片与标题冲突——优先信图片，标记待核实

## 规则结论

当产品图片和标题对某个参数/分类的描述不一致时，优先信图片（图片是实物证据）。标记"待核实"而不是硬判。标题写USB但图片显示Type-C时，填"Type-C有线"，来源写"图片判断"。

## 错误表现

1. 标题写"USB Charging"，图片显示Type-C接口 → 填"USB"（❌应该填"Type-C有线"）
2. 标题说"Wireless"但图片显示有充电口 → 不标记直接按标题填
3. 图片与标题冲突时硬判一个而不标注"待核实"
4. 标题写"Smart Glasses with Camera"但图片明显无摄像头→不验证

## 正确做法

- 图片 vs 标题冲突 → 优先信图片
- 来源标注："图片判断"
- 标题写USB但图片显示Type-C → "Type-C有线，来源：图片判断"
- 标题写USB但无法从图片确认接口 → "USB-接口未确认"
- 无法从图片或标题确认 → "待核实"
- 图片明显显示无某功能（如无摄像头）而标题暗示有 → 以图片为准

## 适用场景

所有需要从产品图片验证参数的场景。

## 禁止再犯

是。

## 正确示例

- ✅ 标题: "USB Charging" + 图片: Type-C口 → 充电方式: Type-C有线，来源: 图片判断
- ✅ 标题: "Smart Glasses" + 图片: 无摄像头 → 产品类型: 音频眼镜（图片优先）
- ✅ 标题冲突+图片模糊 → 待核实

## 错误示例

- ❌ 图片显示Type-C但填"USB"（因标题写USB）
- ❌ 冲突时不标记直接硬判

## 来源证据

- 威猛先生宪法铁律49：图片与标题冲突，必须待核实
- category-fields.md校验规则2：图片和标题冲突，标记"待核实"，优先信图片
- category-fields.md校验规则3：标题写USB但图片显示Type-C，填"Type-C有线"，来源写"图片判断"

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |