---
id: KB-ANTI-LAZY-001
title: 禁止用正则猜参数——卖家精灵详细参数有就不用猜
type: rule（规则）
category: source_rules（来源规则）
tags: [偷懒, 正则, 详细参数, 标题匹配, 卖家精灵]
roles: [Commander, Product Analyst, data-analyst]
status: pending（待审核）
confidence: A（多次发生+Commander修正）
source: memory: "卖家精灵详细参数列是Key:value格式的结构化数据金矿，必须逐项解析"
evidence: 多个类目详细参数被跳过，只用了标题正则
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-SOURCE-004, KB-ANTI-FAKE-001]
---

# 禁止用正则猜参数——卖家精灵详细参数有就不用猜

## 错误表现

卖家精灵导出的"详细参数"列是 Key:value 格式的结构化数据，每个产品约36个标准字段。但偷懒时：
- 只看标题和五点
- 用正则从标题匹配参数
- 详细参数列有Connector Type: USB-C，却在标题找"USB"填成笼统值

## 正确做法

1. 先解析详细参数列（逐行Key:value）
2. 没有的字段再从五点提取
3. 仍没有的从Amazon参数表补充
4. 最后才从标题确认
5. 标题正则永远不是首选数据源

## 适用场景

所有使用卖家精灵导出数据的任务。

## 禁止再犯

是。

## 来源证据

- KB-SOURCE-004: 卖家精灵详细参数列——Key:value格式的结构化金矿
- 威猛先生memory

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |