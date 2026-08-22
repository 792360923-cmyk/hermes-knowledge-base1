---
id: KB-SOURCE-002
title: 卖家精灵Coupon列——%和$两种格式须正确换算
type: rule（规则）
category: source_rules（来源规则）
tags: [卖家精灵, Coupon, 有效价, 换算, 子代理]
roles: [Commander, data-analyst, Data Verifier]
status: pending（待审核）
confidence: A（用户纠正 + 历史返工记录）
source: 威猛先生 memory记录 + BSR调研实践
evidence: BSR调研坑——卖家精灵Coupon列有%和$两种格式，子代理常算错
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-SOURCE-001, KB-ANTI-FAKE-001]
---

# 卖家精灵Coupon列——%和$两种格式须正确换算

## 规则结论

卖家精灵导出的Coupon（优惠券）列有两种格式：
- `20% off` = 打八折，不是减$20
- `$5 off` = 直接减$5

子代理/自动脚本经常把 `20% off` 误当成"减$20"来计算有效价，导致价格错误。

## 错误表现

1. `20% off` = 被当成 Coupon=$20 → 有效价=价格-20（❌ 错！应该是 价格 × 0.8）
2. 只看了Coupon列的数字忽略了后面的 `%` 或 `$` 符号
3. 在Excel中所有Coupon都按金额减法处理

## 正确做法

- 检查Coupon列的原始值格式
- `%` 结尾 → 有效价 = 价格 × (1 - 百分比/100)
- `$` 开头 → 有效价 = 价格 - Coupon金额
- 在Excel结论中区分标注："有效价（Coupon后）"
- 总价排序/均价计算统一用有效价（Coupon后），不是标价
- Commander验收时必须抽查Coupon计算是否正确

## 适用场景

所有使用卖家精灵导出数据的BSR调研（第2页/第9页价格分析）。

## 禁止再犯

是。

## 正确示例

- ✅ 价格$39.99，Coupon 20% off → 有效价 $31.99
- ✅ 价格$29.99，Coupon $5 off → 有效价 $24.99
- ✅ Excel标注：价格列保留标价，新增"有效价"列

## 错误示例

- ❌ 价格$39.99，Coupon 20% off → 当成减$20 → 有效价$19.99（严重错误）
- ❌ 所有Coupon统一按金额减法（忽视%格式）
- ❌ 结论中只提标价不提Coupon后有效价

## 来源证据

- 威猛先生记忆记录："卖家精灵Coupon列有'%'和'$'两种格式(20%off≠减$20)，有效价须正确换算，子代理常算错"
- BSR调研坑（总指挥须审）

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |
