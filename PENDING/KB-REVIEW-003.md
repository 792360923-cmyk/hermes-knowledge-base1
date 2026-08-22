---
id: KB-REVIEW-003
title: delegate_task子代理——关键步骤不委托，Commander亲自做
type: rule（规则）
category: source_rules（来源规则）
tags: [子代理, delegate_task, context, 委托, 亲自做]
roles: [Commander]
status: pending（待审核）
confidence: A（用户memory + 调研实践）
source: 威猛先生memory + 多次子代理翻车
evidence: Bike Pumps子代理三层分类合并、Coupon算错
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-REVIEW-001, KB-CLASSIFY-002]
---

# delegate_task子代理——关键步骤不委托，Commander亲自做

## 规则结论

使用delegate_task分派子代理时，以下关键步骤不能委托，必须Commander亲自做：
1. 产品分类（子代理常犯错）
2. Amazon详情页登录验证（Alexa验证）
3. Coupon价格换算审核
4. 最终结论撰写
5. 9项复查

## 子代理能做什么

- 数据采集（从卖家精灵/网页批量抓取）
- 基础字段提取（Brand/Price/BSR等）
- 图片下载
- 差评/Tavily搜索

## 子代理不能做什么

- 产品分类判断（尤其是手动/电动/无刷电机判断）
- 三层分类拆分（产品类型/外观/场景）
- 结论撰写（无全局视角容易空泛）
- Alexa登录验证（需要Lisa账号）
- Coupon换算审核
- 最终复查

## 错误表现

1. 分类委托给子代理→手动误判电动/漏无刷/合并三层
2. Alexa验证委托→子代理无Lisa账号无法完成
3. Coupon换算委托→20%off当减$20
4. 结论委托→空泛无数据支撑

## 正确做法

- 数据采集委托子代理
- 分类Commander自己做（或子代理做初版+Commander审计修正）
- Alexa验证Commander亲自操作
- Coupon审核Commander抽查
- 结论Commander自己写
- 复查Commander自己做

## 适用场景

所有使用delegate_task的调研任务。

## 禁止再犯

是。

## 来源证据

- 威猛先生memory: "子代理context不足致劣质输出时不委托,关键步骤亲自做"
- Bike Pumps子代理分类翻车案例

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |