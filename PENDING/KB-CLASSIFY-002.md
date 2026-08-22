---
id: KB-CLASSIFY-002
title: 子代理分类错误——手动误判电动/漏无刷电机/合并三层分类
type: rule（规则）
category: classification_rules（分类规则）
tags: [子代理, delegate_task, 分类错误, 手动电动, 无刷电机, 三层分类]
roles: [Commander, Product Analyst]
status: pending（待审核）
confidence: A（历史返工记录）
source: 威猛先生memory + Bike Pumps/吹叶机调研返工
evidence: 子代理多次分类翻车，Commander验收修正
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
related: [KB-CLASSIFY-001, KB-CLASSIFY-003]
---

# 子代理分类错误——手动误判电动/漏无刷电机/合并三层分类

## 规则结论

使用delegate_task（委托任务）派发子代理做产品分类时，子代理经常犯三类错误。Commander（总指挥）必须在验收时针对这三类错误专项审计：
1. 手动产品被误判为电动（词边界问题：motorcycle≠motor）
2. 漏判无刷电机（brushless未识别）
3. 三层分类（功能形态→外观造型→使用场景）被合并成一列

## 错误表现

1. "motorcycle pump"标题含"motor"被误判为电动打气泵
2. "electric bike air pump"里的"bike"被误判为"电动车"场景
3. 无刷电机(Brushless)出现在标题/五点但子代理未提取
4. 三层分类（产品类型/外观造型/使用场景）被合并成一列输出
5. 68个产品使用场景全部填"通用"（Bike Pumps实际案例）
6. 子代理的"产品类型"包含括号内的二层信息如"迷你电动打气泵(便携/通用)"

## 正确做法

1. 验收时用Power Source（动力方式）字段单独核对：Battery Powered≠不一定是电动，需确认
2. 验收时搜索"brushless"词边界，确保无刷电机字段不遗漏
3. 三层分类拆成3个独立列，不合并：
   - 列1：产品类型（功能形态）
   - 列2：外观造型（视觉形态）
   - 列3：使用场景（多值，从标题精确提取）
4. "通用"占比>70%说明场景提取偷懒，必须重做

## 适用场景

所有使用delegate_task做BSR分类的任务。

## 禁止再犯

是。

## 正确示例

- ✅ Bike Pumps：手动立式打气筒/迷你电动打气泵/CO2气瓶/配件（Power Source字段独立核对）
- ✅ 三层独立列：产品类型=迷你电动打气泵 | 外观=迷你 | 场景=公路车、山地车、摩托车
- ✅ 无刷电机：DSUY/GPUTEK提取了brushless标签

## 错误示例

- ❌ "Woowind电动打气泵"（实际是手动立式，标题有pump但不是electric）
- ❌ 产品类型="迷你电动打气泵(便携/通用)"（二层合并进一列）
- ❌ 68个使用场景="通用"（偷懒了）

## 来源证据

- 威猛先生memory: "delegate_task子代理分类易把手动误判电动/漏无刷电机/合并三层分类，须用Power Source字段+brushless词边界审计"
- Bike Pumps v3→v4：子代理三层分类合并→Commander拆分重做
- 吹叶机：5个类型（手持电池式/有线插电式/吹吸两用/三合一/背包式）

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |