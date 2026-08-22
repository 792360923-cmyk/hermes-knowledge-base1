---
id: KB-ANTI-LAZY-007
title: 禁止子代理context不够硬上——关键步骤亲自做
type: rule（规则）
category: source_rules（来源规则）
tags: [偷懒, 子代理, delegate_task, context, 亲自做]
roles: [Commander]
status: pending（待审核）
confidence: A（用户memory+多次子代理翻车）
source: 威猛先生memory
evidence: "子代理context不足致劣质输出时不委托，关键步骤亲自做"
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-REVIEW-003, KB-CLASSIFY-002]
---

# 禁止子代理context不够硬上——关键步骤亲自做

## 错误表现

子代理没有足够上下文（产品判断标准、分类规则、用户偏好），但仍然委托它执行。结果劣质输出，Commander还得翻工重做，比直接自己做花的时间还多。

## 正确做法

- 数据采集（批量抓取）→ 可委托子代理
- 分类判断 → 子代理做初版 + Commander审计
- Alexa验证 → Commander亲自（需要密码）
- 结论撰写 → Commander亲自
- 最终复查 → Commander亲自
- 如果子代理输出明显劣质，直接放弃，Commander从头做
- 委托成本 > 自己做成本时，不委托

## 适用场景

所有delegate_task使用场景。

## 禁止再犯

是。

## 来源证据

- 威猛先生memory: "子代理context不足致劣质输出时不委托，关键步骤亲自做"
- KB-REVIEW-003: delegate_task子代理关键步骤不委托

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |