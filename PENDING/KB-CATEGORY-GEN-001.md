---
id: KB-CATEGORY-GEN-001
title: BSR调研通用流程——卖家精灵导出覆盖全部前100
type: knowledge（知识）
category: category_knowledge（类目知识）
tags: [BSR, 卖家精灵, 导出, Amazon懒加载, 全量]
roles: [Commander, data-analyst]
status: pending（待审核）
confidence: A（多类目实践验证）
source: 威猛先生memory + 多次BSR调研实践
evidence: 吹叶机/Bike Pumps/挂烫机/智能眼镜均用此方法
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-SOURCE-001, KB-SOURCE-004]
---

# BSR调研通用流程——卖家精灵导出覆盖全部前100

## 规则结论

Amazon BSR页面有懒加载机制，只渲染前30-50个产品。不要逐页抓取Amazon详情页。直接使用卖家精灵导出——卖家精灵导出含全部BSR前100+标题翻译+五点+详细参数+主图+A+页面+视频+月销量+月销售额，一站式覆盖所有字段。

## 数据采集流程

1. 卖家精灵导出一份BSR前100全量Excel
2. 解析"详细参数"列（Key:value格式，~36个标准字段）
3. 提取五点和产品卖点
4. 保留卖家精灵独有的字段：月销量/月销售额/FBA运费/大类排名/上架时间
5. 对于关键竞对产品（3-8个头部），Amazon详情页验证参数
6. Alexa补充五点缺失的参数

## 懒加载陷阱

- Amazon BSR页面JS懒加载只渲染30-50个产品
- 逐页抓取会遗漏大量产品
- browser_navigate爬Amazon常被block
- 卖家精灵一键导出比逐页Browser抓取快100倍

## 禁止

- 禁止逐页抓取Amazon详情页（浪费时间+被封风险）
- 禁止跳过卖家精灵详细参数列
- 禁止只用browser_navigate不用卖家精灵导出

## 适用场景

所有Amazon BSR前100调研。

## 禁止再犯

是。

## 来源证据

- 威猛先生memory: "Amazon BSR懒加载只渲染30/50产品。卖家精灵导出含全部BSR前100+标题翻译+五点+参数+主图+A+/视频+月销，勿逐页抓Amazon详情页。"

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |