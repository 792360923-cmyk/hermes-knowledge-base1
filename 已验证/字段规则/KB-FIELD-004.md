---
id: KB-FIELD-004
title: 防水字段细分——IPX4/IPX5/IPX6/IPX7/IP67/未标注
type: rule（规则）
category: field_rules（字段规则）
tags: [防水, IPX, IPXX, 防水等级, 未标注]
roles: [Commander, Product Analyst, Data Verifier]
status: verified（已验证）
confidence: A（用户宪法铁律 + category-fields.md）
source: 威猛先生宪法铁律76-77
evidence: 智能眼镜/吹叶机/挂烫机等类目实践
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 威猛先生（2026-08-22审核通过）
related: [KB-FIELD-001, KB-FIELD-002]
---

# 防水字段细分——IPX4/IPX5/IPX6/IPX7/IP67/未标注

## 规则结论

防水字段必须从笼统的"防水""防水功能"拆到具体IP等级。禁止只写"防水""防水设计""IPX防水"。

## 强制细分

- IPX0（无防护）
- IPX4（防溅水）
- IPX5（防喷水）
- IPX6（防强力喷水）
- IPX7（短时间浸水1m/30min）
- IPX8（持续浸水）
- IP67（防尘+浸水）
- "Water Resistant"但无具体IP → 标注"Water Resistant（无IP等级）"
- 未标注（页面没提防水）
- 无（明确写了"Not Waterproof"）

## 错误表现

1. 填"防水"（不知道IP等级）
2. 填"IPX"（没写数字）
3. 标题说"Waterproof"但没IP等级 → 直接填"有"（应该标注"无IP等级"）

## 正确做法

- 来源：Product Overview > Waterproof Rating / IP Rating
- 来源：Amazon五点/A+
- "Water Resistant"和"Waterproof"不同 → 必须标注有无IP认证
- 中文翻译不改变原意：Water Resistant = 防溅水（非防水）

## 适用场景

所有涉及户外/水接触的产品。

## 禁止再犯

是。

## 来源证据

- 威猛先生宪法铁律76-77：禁止只写"防水"，防水必须细分IPX4/IPX5/IPX6/IPX7/IP67/未标注
- category-fields.md v3.0认证合规字段

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |