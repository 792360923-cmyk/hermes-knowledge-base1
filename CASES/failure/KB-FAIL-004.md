---
id: KB-FAIL-004
title: Discord发.xlsx收不到——必须.zip打包
type: case（案例）
category: source_rules（来源规则）
tags: [失败案例, Discord, .xlsx, .zip, 文件传输]
roles: [Commander, dev-engineer]
status: verified（已验证）
confidence: A（实际发生+用户反馈）
source: 威猛先生memory
evidence: "Discord对.xlsx直接发送会失败(用户收不到)，需先压缩成.zip再发"
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 威猛先生（2026-08-22审核通过）
related: [KB-TABLE-001]
---

# Discord发.xlsx收不到——必须.zip打包

## 错误表现

直接通过Discord MEDIA发送.xlsx文件，用户收不到。发送后用户说"没收到""从发我"。

## 正确做法

- 先用zipfile压缩为.zip
- MEDIA发送.zip文件
- 文件超过3MB → 改短路径（如 /root/bp.zip 而不是 /root/Bike_Pumps_BSR_v3.xlsx）
- txt/图片可直发，不需压缩

## 适用场景

所有Discord文件交付。

## 禁止再犯

是。

## 来源证据

- 威猛先生memory: "MEDIA发文件：Discord对.xlsx直接发送会失败(用户收不到)，需先压缩成.zip再发(steamer_kw.zip成功)。txt/图片可直发。文件超3MB改短路径。"

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |