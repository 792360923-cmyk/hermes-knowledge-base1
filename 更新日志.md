# 更新日志

> 所有知识库变更记录。按时间倒序。

---

## [2026-08-22] 历史复盘全量入库完成 | 10批44条知识卡片

### 总计
- 第1批 最高铁律与防偷懒：3条
- 第2批 数据真实性与来源：5条
- 第3批 产品分类规则：5条
- 第4批 字段拆分规则：5条
- 第5批 表格/Excel规则：5条
- 第6批 角色协作与复查：5条
- 第7批 类目专项经验：5条
- 第8批 知识库/低Token：5条
- 第9批 历史失败案例：4条
- 第10批 成功方法：2条

### 统计
- 规则 30条 / 知识 5条 / 失败案例 4条 / 成功案例 2条 / 合计 44条

### 提交记录（commit）
- `c28fa79` `3616e77` `4157c0a` `3b69e24` `a75c594` `9602ece` `5636e32` `67f9d5e`

### 审核结果
- 全部 pending（待审核），等威猛先生审核后升级正式规则库

---

---

## [2026-08-22] 历史复盘入库第1批 | 最高铁律与防偷懒规则

### 新增
- KB-ANTI-FAKE-001: 禁止编造数据——宁Unknown不硬填
- KB-ANTI-FAKE-002: 来源标注规则——每个关键字段必须标注来源
- KB-ANTI-FAKE-003: 未标注≠无——区分未标注和无

### 审核结果
- 待用户审核（全部为 pending）

### 提交记录（commit）
- `c28fa79`

---

## [2026-08-22] 历史复盘入库第2批 | 数据真实性与来源规则

### 新增
- KB-SOURCE-001: 数据来源优先级——Amazon参数表第一
- KB-SOURCE-002: 卖家精灵Coupon列——%和$两种格式须正确换算
- KB-SOURCE-003: Alexa来源标注——可信度低于listing正文
- KB-SOURCE-004: 卖家精灵详细参数列——Key:value格式的结构化金矿
- KB-SOURCE-005: BSR和销量——大类/小类/父体/子体不能混用

### 审核结果
- 待用户审核（全部为 pending）

### 提交记录（commit）
- `3616e77`

---

## [2026-08-22] 规则新增 | 省Token自成长机制 + 中文化规则

### 新增
- SYS-005 省Token自成长机制（四级读取模式、增量沉淀、错误优先、审核机制）
- SYS-006 中文化规则（交付中文化、状态中英对照、可信等级中英对照）

### 修改
- INDEX.md：表头中文化 + 常驻短规则嵌入
- templates/knowledge_card_template.md：中文化
- templates/review_template.md：中文化
- templates/changelog_template.md：中文化

### 审核结果
- 通过（威猛先生亲自制定规则）

### 提交记录（commit）
- （待提交）

### 关联
- [[SYS-005]]
- [[SYS-006]]

---

## [2026-08-21] 初始化 | 知识库创建

### 新增
- 创建仓库 `hermes-knowledge-base1`
- 初始化目录结构：SYSTEM_RULES/, PENDING/, VERIFIED/（含7个子目录）, REJECTED/, OUTDATED/, CASES/, REVIEW_QUEUE/, templates/
- SYS-001 最高铁律
- SYS-002 角色体系执行规则
- SYS-003 数据真实性规则
- SYS-004 复查与交付规则
- 模板：知识卡片、审查报告、更新日志
- README.md, INDEX.md, CHANGELOG.md
- 定义自生长流程：识别→写入→验证→审核→归档→更新索引

### 提交记录（commit）
- `b5b911e` init: hermes self-growing llmwiki knowledge base