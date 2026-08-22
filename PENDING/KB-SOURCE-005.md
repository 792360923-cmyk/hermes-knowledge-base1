---
id: KB-SOURCE-005
title: BSR和销量——大类/小类/父体/子体不能混用
type: rule（规则）
category: source_rules（来源规则）
tags: [BSR, 大类排名, 小类排名, 父体, 子体, 销量]
roles: [Commander, Market Researcher, Data Verifier]
status: pending（待审核）
confidence: B（Amazon/卖家精灵数据支撑）
source: 威猛先生质量宪法铁律106-110（单位铁律）+ 多次调研实践
evidence: Bike Pumps/吹叶机BSR分析中多次区分大小类排名
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-SOURCE-001, KB-ANTI-FAKE-001]
---

# BSR和销量——大类/小类/父体/子体不能混用

## 规则结论

- 大类BSR（Best Sellers Rank）和小类BSR（Subcategory Rank）是两个不同指标，不能混在一起排序/对比
- 父体销量和子体销量不能混合计算
- 月销量和日销量不能混用
- 当前价格和Coupon后价格不能混用

## 错误表现

1. 用大类BSR和小类BSR混排"Top50"
2. 把父体的月销量当成某个子体的月销量
3. 把日销量×30估算月销量，不标注"估算"
4. 用标价排序/均价计算，忽略了Coupon

## 正确做法

- BSR对比统一用大类BSR，或统一用小类BSR，不能混用
- 销量对比统一用月销量
- 价格分析统一用有效价（Coupon后）
- 父体/子体分开标注，不混合
- 如果数据源只有大类BSR，不在结论中引用小类BSR

## 适用场景

所有Amazon BSR分析和市场调研。

## 禁止再犯

是。

## 正确示例

- ✅ 按大类BSR排序Top50
- ✅ 标价$39.99，有效价$31.99（Coupon 20% off）
- ✅ 月销量=卖家精灵直接导出（非估算）
- ✅ 父体ASIN: B0XXX、子体ASIN: B0YYY 分开标记

## 错误示例

- ❌ "BSR#1是大类第5"混用"小类BSR#3"
- ❌ 日销量×30=月销量（未标注"估算"）
- ❌ 标价排序（忽略Coupon对消费者决策的影响）

## 来源证据

- 威猛先生质量宪法铁律106-110：大类BSR和小类BSR不能混用、父体销量和子体销量不能混用、当前价格和Coupon后价格不能混用

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |
