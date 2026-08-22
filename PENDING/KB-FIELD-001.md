---
id: KB-FIELD-001
title: 充电方式必须细分到具体接口——禁止只写USB
type: rule（规则）
category: field_rules（字段规则）
tags: [充电方式, USB, Type-C, Micro USB, 磁吸, 触点, 细分]
roles: [Commander, Product Analyst, Data Verifier]
status: pending（待审核）
confidence: A（用户宪法铁律 + category-fields.md）
source: 威猛先生宪法铁律66-67 + category-fields.md v3.0充电方式强制细分
evidence: 多类目被要求细分充电方式
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-FIELD-002, KB-FIELD-003, KB-CLASSIFY-001]
---

# 充电方式必须细分到具体接口——禁止只写USB

## 规则结论

充电方式必须从笼统的"USB"拆到具体接口方式。14种细分类型必须全部覆盖。禁止只写"USB""充电""无线"。从详细参数的Connector Type字段或Product Overview参数表读取。

## 14种强制细分

- Type-C有线 / USB-C
- Micro USB有线
- Lightning有线
- DC圆口
- 磁吸充电（Magnetic Charging）
- 触点充电（Pogo Pin）
- 充电盒/充电仓充电（Charging Case）
- 无线充电（Qi Wireless）
- 太阳能充电（Solar）
- 可换电池（Replaceable Battery，非充电电池）
- 干电池（Disposable Battery）
- 纽扣电池（Coin Cell）
- 插电式（AC Plug-in，不带电池）
- USB-接口未确认（只看到USB字样但无法确认Type-C还是Micro）

## 错误表现

1. 填"USB"（不知道是Type-C还是Micro）
2. 填"充电"（不知道是有线还是无线）
3. 填"无线"（不知道是Qi还是磁吸）
4. 填"Type-C"但实际只看到USB字样无法确认接口

## 正确做法

- 来源：详细参数的Connector Type字段
- 来源：Product Overview参数表
- 来源：图片判断（图片显示Type-C口）
- USB-接口未确认 ≠ Type-C（图片无法确认时不能用Type-C）
- 有充电盒的产品，标注"充电盒充电(Type-C)"两个维度

## 适用场景

所有带电产品的充电方式字段。

## 禁止再犯

是。

## 来源证据

- 威猛先生宪法铁律66-67：禁止只写"USB"，USB必须细分Type-C/Micro USB/Lightning/磁吸/触点/充电盒/接口未确认
- category-fields.md v3.0完整充电方式细分清单

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |