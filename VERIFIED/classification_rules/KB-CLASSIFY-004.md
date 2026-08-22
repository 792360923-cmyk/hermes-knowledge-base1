---
id: KB-CLASSIFY-004
title: 配件不能当整机——套装必须判断是否含主机
type: rule（规则）
category: classification_rules（分类规则）
tags: [配件, 整机, 套装, 主机, 误判]
roles: [Commander, Product Analyst, Data Verifier]
status: verified（已验证）
confidence: A（宪法铁律+多类目实践）
source: 威猛先生宪法铁律47+挂烫机规则9
evidence: 挂烫机分类规则9：配件/收纳袋/水杯/刷头/替换件不是整机
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 威猛先生（2026-08-22审核通过）
related: [KB-CLASSIFY-001, KB-ANTI-FAKE-001]
---

# 配件不能当整机——套装必须判断是否含主机

## 规则结论

配件（收纳袋/刷头/替换件/充电底座/充电线/贴片）不能归为整机。套装必须判断是否含完整主机。不含主机的套装也是配件。

## 错误表现

1. 挂烫机类目：收纳袋/水杯/刷头/替换件被当成整机挂烫机
2. 智能眼镜：充电底座/夹片式配件被归入眼镜整机
3. CO2气瓶充气套件被当成"打气筒"（实际无打气筒主体）
4. 套装不含主机也按整机分类（如"Camera glasses accessories"）

## 正确做法

- 挂烫机类目规则：如果只是配件、收纳袋、水杯、刷头、替换件，不是整机，归为"配件"
- 智能眼镜：如果有charging stand/dock/clip-on/accessories等词且不含完整眼镜→配件
- Bike Pumps：CO2气瓶如果没有充气主体→CO2气瓶（不算打气筒整机）
- 套装必须检查是否含主机（详细参数里的"Included Components"字段）
- 不含主机的套装 = 配件

## 适用场景

所有Amazon产品调研的分类环节。

## 禁止再犯

是。

## 正确示例

- ✅ 挂烫机收纳袋 → 配件（不含挂烫机主体）
- ✅ 智能眼镜充电底座 → 配件（不含眼镜）
- ✅ 挂烫机替换刷头 → 配件
- ✅ "Camera Glasses with Charging Case" → 整机（含眼镜主体+充电盒）
- ✅ "Replacement Ear Tips for Glasses" → 配件（替换耳塞不含眼镜）

## 错误示例

- ❌ 挂烫机替换刷头 → 手持式蒸汽挂烫机（❌不含整机主体）
- ❌ CO2充气套件 → 手动打气筒（❌实际无打气筒，只是气瓶+充气头）

## 来源证据

- 威猛先生宪法铁律47：配件不能归为整机
- 挂烫机10条分类规则第9条：配件/收纳袋/水杯/刷头/替换件不是整机

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-22 | 初始创建 | Commander |