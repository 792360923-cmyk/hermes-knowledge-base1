---
id: KB-SOURCE-001
title: 数据来源优先级——Amazon参数表第一
type: rule（规则）
category: source_rules（来源规则）
tags: [数据来源, 优先级, Product Overview, 卖家精灵, Alexa]
roles: [Commander, Product Analyst, Market Researcher, Data Verifier]
status: verified（已验证）
confidence: A（用户多次明确要求）
source: category-fields.md v3.0 + 历史任务实践
evidence: 字段库明确写入，多类目（吹叶机/Bike Pumps/挂烫机）实际执行
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 威猛先生（2026-08-22审核通过）
related: [KB-ANTI-FAKE-001, KB-SOURCE-002, KB-SOURCE-003]
---

# 数据来源优先级——Amazon参数表第一

## 规则结论

数据来源有明确的优先级排序。当多个来源对同一参数有矛盾时，按优先级取最高者。低优先级来源仅作为补充。

## 来源优先级（从高到低）

1. **Amazon Product Overview 参数表**（最高可信度）
2. **卖家精灵详细参数列**（Key:value结构化数据）
3. **Amazon五点卖点**（listing正文）
4. **Amazon标题**
5. **图片识别**（信息图/副图上的参数标注）
6. **Alexa购物助手问答**（需标注"Alexa来源"，可信度低于listing正文）
7. **Review/Q&A**（仅供参考，不能作为硬参数来源）

## 错误表现

1. 用Alexa回答覆盖Product Overview参数表数据
2. 卖家精灵有详细参数不用，直接从标题正则提取
3. Review里有人说"续航2小时"就填2小时
4. 五点写了"1200mAh"，图片显示"1500mAh"时不标记待核实

## 正确做法

- 先从Amazon Product Overview参数表读取
- 参数表没有的，从卖家精灵详细参数读取
- 仍没有的，从五点提取
- 标题才能确认的，标记为"标题来源"（可信度较低）
- Alexa补充的字段，必须标注"Alexa来源"
- Review/Q&A信息只用于痛点/好评分析，不用于参数填充

## 适用场景

所有Amazon产品调研的参数提取。

## 禁止再犯

是。

## 正确示例

- ✅ 来源：Amazon Product Overview参数表 → 电压: 20V
- ✅ 来源：卖家精灵详细参数 → Connector Type: USB-C（标题写USB但参数表明确Type-C）
- ✅ 来源：Alexa来源 → 续航: 约90min（low speed）（五点未标注，Alexa补充）

## 错误示例

- ❌ 来源：Review → 电池: 2000mAh（review不一定准）
- ❌ 来源：Alexa（未标注，当成确定参数）
- ❌ 从标题正则提取参数（可能误判，如"motorcycle pump"≠电机驱动）

## 来源证据

- category-fields.md v3.0 明确写入数据来源优先级
- 吹叶机调研：Amazon参数表验证8个头部产品的CFM/MPH/电机/噪音/续航
- Bike Pumps调研：修正了子代理错把"motorcycle pump"当电动的分类错误

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |
