# PENDING（待审核区）— 待审核知识

> 所有新识别的经验先写入此目录，经 Data Verifier 验证 + Commander 审核后才能移入正式规则库。

## 历史复盘入库（2026-08-22）

| ID | 标题 | 批次 | 提交日期 | 状态 |
|----|------|------|---------|------|
| KB-ANTI-FAKE-001 | 禁止编造数据——宁Unknown不硬填 | 第1批 | 2026-08-22 | pending（待审核） |
| KB-ANTI-FAKE-002 | 来源标注规则——每个关键字段必须标注来源 | 第1批 | 2026-08-22 | pending（待审核） |
| KB-ANTI-FAKE-003 | 未标注≠无——区分未标注和无 | 第1批 | 2026-08-22 | pending（待审核） |
| KB-SOURCE-001 | 数据来源优先级——Amazon参数表第一 | 第2批 | 2026-08-22 | pending（待审核） |
| KB-SOURCE-002 | 卖家精灵Coupon列——%和$两种格式须正确换算 | 第2批 | 2026-08-22 | pending（待审核） |
| KB-SOURCE-003 | Alexa来源标注——可信度低于listing正文 | 第2批 | 2026-08-22 | pending（待审核） |
| KB-SOURCE-004 | 卖家精灵详细参数列——Key:value格式的结构化金矿 | 第2批 | 2026-08-22 | pending（待审核） |
| KB-SOURCE-005 | BSR和销量——大类/小类/父体/子体不能混用 | 第2批 | 2026-08-22 | pending（待审核） |

## 审核流程

1. Hermes 任务完成 → 识别新经验
2. 按 `templates/knowledge_card_template.md` 格式写入
3. Data Verifier 验证来源
4. Commander 审核
5. 通过 → 正式规则库 | 驳回 → 已拒绝区