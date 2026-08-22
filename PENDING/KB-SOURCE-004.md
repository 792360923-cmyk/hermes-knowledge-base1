---
id: KB-SOURCE-004
title: 卖家精灵详细参数列——Key:value格式的结构化金矿
type: rule（规则）
category: source_rules（来源规则）
tags: [卖家精灵, 详细参数, Key:value, 结构化数据]
roles: [Commander, data-analyst, Product Analyst]
status: pending（待审核）
confidence: A（用户多次强调 + BSR调研实践）
source: 威猛先生记忆记录
evidence: 多次任务使用卖家精灵详细参数提取字段
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-SOURCE-001, KB-FIELD-001]
---

# 卖家精灵详细参数列——Key:value格式的结构化金矿

## 规则结论

卖家精灵导出的"详细参数"列是 Key:value 格式的结构化数据，包含约36种标准字段（如 Connector Type / Battery Capacity / Memory Storage / Operating System 等）。必须逐项解析，不能只提取两三个就跳过。

## 错误表现

1. 只看标题/五点，忽略详细参数列
2. 只提取了Brand/Price，忽略了Connector Type/电池信息等
3. 看到Key:value格式觉得"太长了懒得解析"
4. 用正则从标题匹配参数，不用详细参数列的结构化数据

## 正确做法

- 每个产品的"详细参数"列都要逐行解析
- 每行是 `Key: value` 格式
- 常见Key包括：Brand / Manufacturer / Model Name / Color / Material / Power Source / Battery Capacity / Connector Type / Voltage / Wattage / Item Weight / Product Dimensions / Operating System / Memory Storage Capacity / Special Feature / Included Components / Waterproof Rating 等约36种
- 每个Key提取出来成为表格字段列
- 未出现在详细参数中的字段，再从五点/标题/图片补充

## 适用场景

所有使用卖家精灵导出数据的Amazon产品调研。

## 禁止再犯

是。

## 正确示例

- ✅ 详细参数解析 → Connector Type: USB-C、Battery Capacity: 5000mAh、Voltage: 20V
- ✅ 提取16个Key:value对，每个成为独立列
- ✅ 未在详细参数找到的字段，从Amazon参数表补充

## 错误示例

- ❌ "详细参数太长了，我只看了Brand和Material"（偷懒）
- ❌ 只提取3个字段，其余从标题正则猜
- ❌ 详细参数里有Connector Type不用，去标题里找"USB"（不精确）

## 来源证据

- 威猛先生记忆："卖家精灵'详细参数'列是Key:value格式的结构化数据金矿，必须逐项解析"
- 智能眼镜调研：从详细参数中提取了37个专属字段

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |
