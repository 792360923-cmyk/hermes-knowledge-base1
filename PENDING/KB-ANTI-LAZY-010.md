---
id: KB-ANTI-LAZY-010
title: 禁止数据来源不具体——不能只写"网络""亚马逊"
type: rule（规则）
category: source_rules（来源规则）
tags: [偷懒, 来源, 标注, 不具体]
roles: [Commander, Product Analyst, Data Verifier]
status: pending（待审核）
confidence: A（宪法铁律33-34）
source: 威猛先生宪法
evidence: 宪法铁律33"不能只写来源：网络"、34"不能只写来源：亚马逊"
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-ANTI-FAKE-002, KB-SOURCE-001]
---

# 禁止数据来源不具体——不能只写"网络""亚马逊"

## 错误表现

- 来源填"网络"
- 来源填"亚马逊"
- 来源填"卖家精灵"但不具体到哪个字段/哪个列
- 来源填"Amazon标题"但实际数据来自详情页参数表

## 正确做法

来源必须具体到：
- Amazon Product Overview参数表
- Amazon五点第3条
- Amazon图片#2信息图
- 卖家精灵详细参数列 Connector Type字段
- Alexa购物助手问答

## 适用场景

所有需要标注来源的字段。

## 禁止再犯

是。

## 来源证据

- 宪法铁律33-34
- KB-ANTI-FAKE-002

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |