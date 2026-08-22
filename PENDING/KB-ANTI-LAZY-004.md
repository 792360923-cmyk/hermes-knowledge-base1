---
id: KB-ANTI-LAZY-004
title: 禁止字段只提取2-3个——必须穷举维度
type: rule（规则）
category: field_rules（字段规则）
tags: [偷懒, 字段穷举, 维度, 详细参数, 五点]
roles: [Commander, Product Analyst, data-analyst]
status: pending（待审核）
confidence: A（category-fields.md穷举铁律）
source: category-fields.md v3.0 + 多次被要求补充字段
evidence: 字段库明确穷举铁律
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-ANTI-LAZY-001, KB-FIELD-001]
---

# 禁止字段只提取2-3个——必须穷举维度

## 错误表现

卖家精灵详细参数有36个字段，但只提取了Brand/Price/Material就跳过其余的。剩余字段靠猜或直接不填。

## 正确做法

1. 详细参数列中每个Key都是候选字段
2. 有效字段全部提取（通常15-20个以上）
3. 字段库里没有的新卖点当场补充进表
4. 从五点/A+/图片补充详细参数没有的字段

## 判断标准

- 类目不适用 → 不提取
- 类目适用但卖家精灵没数据 → 留空标注"未标注"
- 详细参数里有却跳过 → 偷懒
- 只提3个字段交差 → 返工

## 适用场景

所有数据提取任务。

## 禁止再犯

是。

## 来源证据

- category-fields.md: "穷举铁律：每个出现的卖点逐条提取成独立列（禁止合并细分维度）"

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |