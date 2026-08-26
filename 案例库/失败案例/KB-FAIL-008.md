---
id: KB-FAIL-008
title: String Trimmers调研偷懒——电压兜底22件/竞品6个只核3个/图片缺11张/没交叉验证/没核实电动燃油分类
type: case（案例）
category: classification_rules（分类规则）
tags: [失败案例, 偷懒, 兜底类, Alexa核实不全, 图片缺失, 交叉验证, 分类核实, 打草机, String Trimmers]
roles: [Commander, Product Analyst, Data Verifier]
status: pending（待审核）
confidence: A（实际发生+用户亲自纠正）
source: String Trimmers BSR调研记录
evidence: 威猛先生2026-08-26质问"有没有偷懒？"，要求"必须遵循铁律来 再偷懒开除你"
created_at: 2026-08-26
updated_at: 2026-08-26
reviewed_by: 待审核
related: [KB-FAIL-005, KB-FAIL-006, KB-CLASSIFY-001]
---

# String Trimmers 调研偷懒——电压兜底/竞品不全/缺图/无交叉验证

## 错误表现

1. "电池款"兜底22件：电压识别失败全归兜底类，占比22%超10%铁律
2. 6个竞品只核3个(Alexa)：承诺核实却核了3个就急于建表输出
3. 图片缺11张：下载失败没补
4. 没做交叉验证：Alexa结果和卖家精灵没核对
5. 没逐ASIN核实电动/燃油分类：标题推断不够
6. **交付前不自检空值率就发**：写完step2没逐列扫描空值，直接发用户，被质疑"为什么不检查再发/有没有严格按skill"

## 正确做法

1. 兜底<10%：失败必须从Product Overview/Alexa补
2. 竞品全核：选定几个核几个
3. 图片全量：失败重试
4. 交叉验证铁律：Alexa+卖家精灵+Product Overview三方核对
5. 电动/燃油必问Alexa
6. **交付前必跑空值扫描**：表格保存后立即逐列统计空值，总空值率>10%禁止交付，先修复再发

## 后果

22件电压不明 → 分类不准 → 切入建议缺支撑 → 偷懒被用户发现

## 禁止再犯

是。

## 更新记录

| 日期 | 变更 | 操作人 |
|------|------|--------|
| 2026-08-26 | 初始创建 | Commander |