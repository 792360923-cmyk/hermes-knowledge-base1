---
id: KB-FAIL-003
title: Commander重新分类引入新错误——放弃重写用修正
type: case（案例）
category: classification_rules（分类规则）
tags: [失败案例, Commander, 重新分类, 新错误, 修正]
roles: [Commander]
status: pending（待审核）
confidence: A（实际发生）
source: Bike Pumps调研Commander重新分类
evidence: Commander重写分类把Woowind/OGERY误判为手动
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-CLASSIFY-002, KB-REVIEW-003]
---

# Commander重新分类引入新错误——放弃重写用修正

## 错误表现

Bike Pumps调研中，Commander不满意子代理的分类，决定从零重写分类逻辑。但重写引入了新bug：
- Woowind和OGERY被新的正则表达式误判为手动打气筒（实际是电动）
- "electric bike air pump"中的"bike"被误判为电动车场景

## 正确做法

Commander发现后立即停止重写：**放弃从零重写，直接在已验证的子代理版本上做8个争议项的修正**。

## 教训

- 从零重写 > 修正：重写成本高且容易引入新错误
- 修正 > 重写：保留已验证的90%，只改10%有问题的地方
- 修正后功能回归测试：对比修正前后的分布变化

## 适用场景

所有Commander对子代理结果的修正工作。

## 禁止再犯

是。

## 来源证据

- Bike Pumps调研Commander日志

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |