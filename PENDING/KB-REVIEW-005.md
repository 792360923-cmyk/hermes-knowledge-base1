---
id: KB-REVIEW-005
title: Data Verifier验证——所有数据提交前必须验证
type: rule（规则）
category: source_rules（来源规则）
tags: [Data Verifier, 验证, 来源, 真实性, AI推测]
roles: [Data Verifier, Commander]
status: pending（待审核）
confidence: A（用户宪法铁律132 + 角色体系）
source: 威猛先生质量宪法+角色体系
evidence: Amazon AI Team角色体系中的Data Verifier职责
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-REVIEW-001, KB-REVIEW-002]
---

# Data Verifier验证——所有数据提交前必须验证

## 规则结论

所有数据在进入最终报告前，必须经过Data Verifier验证。未经验证的数据禁止进入最终报告。

## 验证8项检查

1. 数据是否有来源 → 来源缺失必须退回
2. 数字是否真实 → 疑似编造必须退回
3. 公式是否正确 → Coupon/汇率/单位换算
4. 分类是否合理 → 物理形态vs营销词
5. 单位是否统一 → lb/kg混用必须更正
6. 是否存在编造 → 直接写数据的无来源值
7. 是否存在未标注硬填 → "应该""估计""大约"
8. 是否存在AI推测冒充事实 → "行业一般""我判断"

## 错误表现

1. Data Verifier只盖章不检查
2. 发现无来源数据放行
3. 怀疑编造不退回
4. 跳过Data Verifier直接交付

## 正确做法

- 每批数据进入报告前，Data Verifier逐个检查来源
- 不通过 → 退回重新采集
- 验证通过的标注"Data Verifier验证通过"
- 部分通过标注"X个字段待补充"

## 适用场景

所有Amazon调研任务（尤其是Amazon AI Team模式）。

## 禁止再犯

是。

## 来源证据

- 威猛先生质量宪法铁律132：未经Data Verifier验证禁止交付
- Amazon AI Team角色体系：Data Verifier职责

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |