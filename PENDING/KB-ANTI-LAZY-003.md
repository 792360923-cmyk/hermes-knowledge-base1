---
id: KB-ANTI-LAZY-003
title: 禁止场景全填"通用"——使用场景必须从标题精确提取
type: rule（规则）
category: classification_rules（分类规则）
tags: [偷懒, 使用场景, 通用, 标题提取, 多值]
roles: [Commander, Product Analyst]
status: pending（待审核）
confidence: A（Bike Pumps返工案例）
source: Bike Pumps v3→v4返工
evidence: 子代理把68个产品场景填"通用"，Commander从标题重提取
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-FAIL-002, KB-CLASSIFY-002]
---

# 禁止场景全填"通用"——使用场景必须从标题精确提取

## 错误表现

Bike Pumps调研中，子代理把68个产品（95%）的使用场景全部填为"通用"。

## 正确做法

1. 从标题提取多场景关键词
   - road bike → 公路车
   - mountain bike/MTB → 山地车
   - motorcycle → 摩托车
   - ball → 球类
   - car → 汽车
   - shock/fork → 避震器
2. 一个产品可以对应多个场景
3. 场景列允许多值（用、分割）

## 判断标准

- "通用"占比 > 50% = 偷懒信号
- "通用"占比 > 70% = 必须重做

## 适用场景

所有BSR调研的使用场景提取。

## 禁止再犯

是。

## 来源证据

- KB-FAIL-002: 子代理三层分类合并
- Bike Pumps v3→v4 Commander场景重提取

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |