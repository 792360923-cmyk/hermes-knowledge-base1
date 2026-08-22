---
id: KB-SOURCE-003
title: Alexa来源标注——可信度低于listing正文
type: rule（规则）
category: source_rules（来源规则）
tags: [Alexa, 购物助手, 可信度, 来源标注]
roles: [Commander, Product Analyst, Data Verifier]
status: verified（已验证）
confidence: A（用户明确要求 + 多次实践）
source: 威猛先生记忆记录 + 多次任务使用Alexa验证
evidence: 挂烫机/吹叶机/Bike Pumps等多个类目使用Alexa
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 威猛先生（2026-08-22审核通过）
related: [KB-SOURCE-001, KB-ANTI-FAKE-002]
---

# Alexa来源标注——可信度低于listing正文

## 规则结论

Amazon Alexa（Rufus购物助手）的回答可以补充五点中未提及的参数，但可信度低于listing正文（标题/五点/Product Overview）。使用Alexa数据时必须标注"Alexa来源"。

## Alexa 能做什么

- Listing五点没有写的参数，如夜灯、亮度调节、静音dB、覆盖面积等
- 产品功能细节，如遥控方式、APP控制范围
- 提供比五点更丰富的参数描述（如Fajuod五点只写"3色氛围灯"，但Alexa答出"Brightness control via remote/app/touch"）
- 可以从产品描述/QA/评论综合提取参数

## Alexa 的限制

- 可信度低于listing正文
- 回答可能不准确或过时
- 不能作为唯一确认来源
- 答案需与图片/A+等其他来源交叉验证

## 正确做法

- 使用Alexa：当五点/参数表缺失某些关键参数时
- 标注方式：`来源：Alexa来源`
- 有条件的字段：`来源：Alexa来源（需二级验证）`
- 不与listing正文冲突时，可以使用Alexa数据
- 与listing正文冲突时，以listing正文为准

## 适用场景

Amazon产品详情页参数提取，尤其是五点及参数表覆盖不到的细节功能。

## 禁止再犯

是。

## 正确示例

- ✅ 来源：Amazon五点 → 3色氛围灯 | 来源：Alexa来源 → 亮度调节方式：遥控/APP/触控
- ✅ 来源：Alexa来源（需二级验证）→ 续航：约90min（低速档）
- ✅ 来源：Alexa来源 → 噪音dB：65dB（五点未标注）

## 错误示例

- ❌ 只用Alexa回答，不标注来源
- ❌ Alexa说"有蓝牙"，不验证就填（可能有错）
- ❌ Alexa回答覆盖了listing正文的明确参数

## 来源证据

- 威猛先生记忆："五点缺参数字段时先问Alexa,答出的标'Alexa来源'(可信度低于listing正文)"
- Fajuod产品案例：五点只写3色氛围灯但Alexa答出完整控制方式

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |
