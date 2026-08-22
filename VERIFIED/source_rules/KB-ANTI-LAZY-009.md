---
id: KB-ANTI-LAZY-009
title: 禁止用browser_navigate代替卖家精灵——BSR懒加载只渲染30个
type: rule（规则）
category: source_rules（来源规则）
tags: [偷懒, browser_navigate, 卖家精灵, BSR, 懒加载]
roles: [Commander, dev-engineer]
status: verified（已验证）
confidence: A（用户memory+实践验证）
source: 威猛先生memory
evidence: "Amazon BSR懒加载只渲染30/50产品。卖家精灵导出含全部BSR前100，勿逐页抓Amazon详情页"
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 威猛先生（2026-08-22审核通过）
related: [KB-CATEGORY-GEN-001, KB-ANTI-LAZY-001]
---

# 禁止用browser_navigate代替卖家精灵——BSR懒加载只渲染30个

## 错误表现

没有用卖家精灵导出，而是用browser_navigate逐页抓取Amazon BSR页面。由于Amazon懒加载只渲染前30-50个产品，导致大量产品遗漏。而且browser_navigate常被Amazon block。

## 正确做法

- 默认用卖家精灵导出BSR前100
- browser_navigate只用于竞对Amazon详情页验证
- 卖家精灵导出 = 全量数据 + 详细参数 + 月销量 + 主图
- browser_navigate = 仅用于补充验证竞对

## 适用场景

所有Amazon BSR调研。

## 禁止再犯

是。

## 来源证据

- 威猛先生memory
- KB-CATEGORY-GEN-001

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |