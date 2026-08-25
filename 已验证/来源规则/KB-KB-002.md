---
id: KB-KB-002
title: PENDING不能自动升级正式规则库——等用户审核
type: rule（规则）
category: source_rules（来源规则）
tags: [PENDING, 正式规则库, 审核, 升级, 用户确认]
roles: [Commander]
status: verified（已验证）
confidence: A（用户亲自制定）
source: 威猛先生省Token自成长机制
evidence: SYS-005第十节用户审核机制
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 威猛先生（2026-08-22审核通过）
related: [KB-KB-001, KB-KB-003]
---

# PENDING（待审核区）不能自动升级正式规则库——等用户审核

## 规则结论

所有PENDING（待审核区）知识必须等用户明确说"审核通过，升级到正式规则库"才能移入正式规则库。用户没有确认前，只能作为pending（待审核），不能作为硬规则、不能强制调用。

## 任务后只做增量沉淀

- 本次犯错 → CASES/failure 或 PENDING（待审核区）
- 本次新规则 → PENDING（待审核区）
- 本次用户明确纠正 → PENDING（待审核区）高优先级
- 本次通过验证的稳定规则 → 等用户确认后再升级正式规则库

## 禁止

- 自动写入正式规则库
- 自动修改旧规则
- 自动删除旧规则
- 自动重写全库
- 自动总结一堆无用知识

## 正确做法

- 知识卡片写入 PENDING/ → status: verified（已验证）
- 审查报告写入 REVIEW_QUEUE/
- 用户说"通过" → 移入正式规则库
- 用户说"驳回" → 移入已拒绝区
- 用户沉默 → 留在PENDING（待审核区），不升级

## 适用场景

所有知识库写入操作。

## 禁止再犯

是。

## 来源证据

- SYS-005第十节
- 威猛先生："所有PENDING知识必须等用户明确说'审核通过，升级到正式规则库'才能进入正式规则库"

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |