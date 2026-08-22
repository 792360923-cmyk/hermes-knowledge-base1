---
id: KB-FAIL-001
title: 子代理Coupon换算错误——20%off当成减$20
type: case（案例）
category: classification_rules（分类规则）
tags: [失败案例, Coupon, 子代理, 换算, 有效价]
roles: [Commander, data-analyst]
status: verified（已验证）
confidence: A（实际发生+用户纠正）
source: BSR调研返工记录
evidence: 威猛先生memory: "卖家精灵Coupon列有%和$两种格式(20%off≠减$20)，有效价须正确换算，子代理常算错"
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 威猛先生（2026-08-22审核通过）
related: [KB-SOURCE-002, KB-REVIEW-003]
---

# 子代理Coupon换算错误——20%off当成减$20

## 错误表现

子代理在分析卖家精灵Coupon列时，把 `20% off` 当成了"减$20"来计算有效价。

## 正确做法

- `20% off` = 有效价 = 价格 × (1 - 0.20)
- `$5 off` = 有效价 = 价格 - $5
- Commander验收时必须抽查Coupon计算

## 后果

- 价格排序错误
- 均价计算错误
- 价格带分布分析错误
- 结论中的价格分析全错

## 适用场景

所有使用卖家精灵导出数据的任务。

## 教训

子代理的Coupon换算不正确是高频错误。Commander必须在首次收到子代理结果时，手动抽查3-5个Coupon产品的有效价是否正确。

## 禁止再犯

是。

## 来源证据

- 威猛先生memory: "BSR调研坑(总指挥须审)：卖家精灵Coupon列有'%'和'$'两种格式(20%off≠减$20)，有效价须正确换算，子代理常算错"

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |