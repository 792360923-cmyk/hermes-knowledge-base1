---
id: KB-FIELD-003
title: 遥控/控制方式细分——遥控器/APP/蓝牙/WiFi/触控/按键
type: rule（规则）
category: field_rules（字段规则）
tags: [遥控, APP, 蓝牙, WiFi, 触控, 按键, 控制方式]
roles: [Commander, Product Analyst, Data Verifier]
status: pending（待审核）
confidence: A（用户宪法铁律 + category-fields.md）
source: 威猛先生宪法铁律70-71
evidence: 智能眼镜/吹叶机等类目实践
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-FIELD-001, KB-CLASSIFY-001]
---

# 遥控/控制方式细分——遥控器/APP/蓝牙/WiFi/触控/按键

## 规则结论

控制方式字段必须从笼统的"遥控""智能控制"拆到具体方式。禁止只写"遥控""智能""无线控制"。

## 强制细分

- 遥控器（红外/无线电物理遥控器）
- APP控制（手机APP/WiFi/蓝牙连接）
- 蓝牙控制
- WiFi控制
- 2.4G无线控制
- 触控（产品本体触摸按键/触摸屏）
- 按键控制（物理按钮）
- 语音控制（Alexa/Google Assistant/Siri）
- 手势控制
- 未标注

## 错误表现

1. 填"遥控"（没说是遥控器还是APP）
2. 填"智能控制"（AI营销词，不是控制方式）
3. 填"无线"（没区分蓝牙/WiFi/2.4G）
4. 有APP控制但没写是否支持iOS/Android

## 正确做法

- 一个产品支持多种控制方式时，填多种（多选字段）
- 来源：Product Overview > Control Method / Human Interface Input
- 来源：Amazon五点/A+
- 例：触控+APP+iOS+Android
- 例：物理按键+遥控器

## 适用场景

所有具有控制功能的产品（灯具/香薰机/智能眼镜/工具等）。

## 禁止再犯

是。

## 来源证据

- 威猛先生宪法铁律70-71：禁止只写"遥控"，遥控必须细分遥控器/APP/蓝牙/WiFi/2.4G/触控/按键
- 智能眼镜：触控/语音/按键/手势四种控制方式独立列

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |