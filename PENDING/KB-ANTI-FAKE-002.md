---
id: KB-ANTI-FAKE-002
title: 来源标注规则——每个关键字段必须标注来源
type: rule（规则）
category: source_rules（来源规则）
tags: [来源, 标注, 数据溯源, 卖家精灵, Amazon, Alexa]
roles: [Commander, Product Analyst, Market Researcher, Keyword Specialist, Data Verifier]
status: pending（待审核）
confidence: A（用户多次明确要求）
source: 威猛先生质量宪法铁律31-40
evidence: 多次任务中被要求标注具体来源
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-ANTI-FAKE-001, KB-FIELD-001]
---

# 来源标注规则——每个关键字段必须标注来源

## 规则结论

每个关键字段必须标注来源，来源必须具体到 Amazon标题/五点/Product Overview/图片/A+/Review/Q&A/卖家精灵/Keepa/用户文件。禁止只写"网络""亚马逊"作为来源。

## 错误表现

1. 只写"来源：网络"
2. 只写"来源：亚马逊"
3. 把别的ASIN数据套到当前ASIN
4. 把父体数据当成子体数据
5. 把类目数据当成单品数据
6. 把样本数据说成全市场数据
7. 把截图看不清的数据写成确定数据

## 正确做法

来源必须具体到：
- Amazon标题、五点、Product Overview、图片（信息图/副图）、A+、Review、Q&A
- 卖家精灵导出数据
- Keepa历史数据
- 用户提供文件/截图
- Alexa购物助手问答（可信度低于listing正文，需标注"Alexa来源"）

示例：
- ✅ 来源：Amazon Product Overview参数表
- ✅ 来源：卖家精灵详细参数列
- ✅ 来源：Amazon图片#3信息图
- ✅ 来源：Alexa问答（需二级验证）

## 适用场景

所有Amazon/ecommerce数据提取任务。

## 禁止再犯

是。

## 来源证据

- 威猛先生质量宪法铁律31-40
- 200条铁律中明确：每个关键字段必须有来源，来源必须具体

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |
