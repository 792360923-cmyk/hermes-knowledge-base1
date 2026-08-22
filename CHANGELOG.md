# 更新日志

> 所有知识库变更记录。按时间倒序。

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