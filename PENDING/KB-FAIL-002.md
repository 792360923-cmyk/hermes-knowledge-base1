---
id: KB-FAIL-002
title: 子代理三层分类合并——产品类型/外观/场景合为一列
type: case（案例）
category: classification_rules（分类规则）
tags: [失败案例, 三层分类, 子代理, 合并列]
roles: [Commander, Product Analyst]
status: pending（待审核）
confidence: A（实际发生+Commander修正）
source: Bike Pumps调研v3→v4返工
evidence: Bike Pumps子代理把三层合并进"产品类型"列，Commander拆分为3独立列
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-CLASSIFY-002, KB-REVIEW-003]
---

# 子代理三层分类合并——产品类型/外观/场景合为一列

## 错误表现

子代理把三层分类合并进"产品类型"列，写成了：
`迷你电动打气泵（便携/通用）`

导致：
- 68个产品使用场景全部填"通用"（偷懒）
- 无法按外观筛选
- 无法按场景筛选
- Excel筛选/透视全废

## 正确做法

三层拆成3个独立列：
1. 产品类型：迷你电动打气泵
2. 外观造型：迷你
3. 使用场景：公路车、山地车、摩托车（多值）

## 后果

Commander不得不重新拆分+从标题重新提取使用场景，"通用"占比从95%降到10%。

## 适用场景

所有使用子代理做三层分类的任务。

## 教训

- 子代理不理解"三层必须独立列"，指令需要非常明确
- Commander验收时第一眼看是否有合并列
- "通用"占比>50%=偷懒信号

## 禁止再犯

是。

## 来源证据

- Bike Pumps v3→v4 Commander修正记录

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |