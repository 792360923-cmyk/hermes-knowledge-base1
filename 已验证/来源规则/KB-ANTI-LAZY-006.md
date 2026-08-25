---
id: KB-ANTI-LAZY-006
title: 禁止不打包.zip直接发.xlsx——Discord收不到
type: rule（规则）
category: source_rules（来源规则）
tags: [偷懒, .zip, .xlsx, Discord, 文件传输]
roles: [Commander, dev-engineer]
status: verified（已验证）
confidence: A（多次发生+用户反馈）
source: 威猛先生memory + 多次返工
evidence: "没收到从发我"——用户反馈
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 威猛先生（2026-08-22审核通过）
related: [KB-FAIL-004, KB-TABLE-001]
---

# 禁止不打包.zip直接发.xlsx——Discord收不到

## 错误表现

做完表格直接用MEDIA发.xlsx文件，用户说"没收到""从发我"。

## 正确做法

- .xlsx → 先 zipfile 压缩为 .zip
- 用简短文件名（/root/bp.zip 不是 /root/Bike_Pumps_Full_Analysis_v3.0.xlsx）
- 文件 > 3MB → 改短路径
- txt/图片可直发，不需压缩

## 适用场景

所有Discord文件交付。

## 禁止再犯

是。

## 来源证据

- 威猛先生memory + KB-FAIL-004

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |