---
id: KB-ANTI-LAZY-002
title: 禁止竞对参数不验证——竞对必须Amazon详情页验证
type: rule（规则）
category: source_rules（来源规则）
tags: [偷懒, 竞对, 验证, Amazon详情页, Alexa]
roles: [Commander, Product Analyst]
status: pending（待审核）
confidence: A（多次任务要求）
source: 威猛先生memory + product-analysis-page2 skill
evidence: 吹叶机/挂烫机/Bike Pumps均要求竞对Amazon验证
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-SOURCE-001, KB-ANTI-LAZY-001]
---

# 禁止竞对参数不验证——竞对必须Amazon详情页验证

## 错误表现

用户指定的竞对产品，只用了卖家精灵数据，没有进Amazon详情页逐项验证参数。

## 正确做法

1. 卖家精灵导出→初步数据
2. 用户指定的竞对ASIN → 必须亲自进Amazon详情页验证
3. 验证内容：Product Overview参数表 + 五点 + 图片/A+ 
4. 用Alexa补充五点缺失的字段
5. 验证后的行标注"Amazon+Alexa✅"

## 适用场景

所有用户指定竞对产品的调研。

## 禁止再犯

是。

## 来源证据

- 吹叶机BSR50: 8个头部产品Amazon详情页逐页验证
- Bike Pumps: DSUY/ETENWOLF竞对Amazon+Alexa验证
- 挂烫机: 竞对B0FYFFPJNS Amazon验证

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |