---
id: KB-ROOT-001
title: Hermes Knowledge Base
type: index
status: verified
confidence: A
created_at: 2026-08-21
updated_at: 2026-08-21
---

# Hermes 自生长知识库

> Hermes Agent 驱动的自生长 LLM Wiki 知识库。
> 用于 Amazon/ecommerce 产品调研、字段库、分类规则、失败经验、提示词模板、角色规则的长期沉淀。

## 理念

- **Markdown + Git + Obsidian 三位一体** — 纯文本，零锁定，任何编辑器可用
- **PENDING → VERIFIED 审核管线** — 所有知识必须经过 Commander + Data Verifier 双重验证
- **自生长** — 每次任务完成后自动识别新经验，写入 PENDING，审核后归档
- **铁律驱动** — 基于 200 条质量宪法，确保每一条知识都有来源有证据

## 目录结构

```
hermes-knowledge-base/
├── README.md              ← 你在这里
├── INDEX.md               ← 知识索引（按分类+状态）
├── CHANGELOG.md           ← 变更日志
├── SYSTEM_RULES/          ← 质量宪法规则
├── PENDING/               ← 待审核知识
├── VERIFIED/              ← 已验证知识（核心库）
│   ├── field_rules/       ← 字段规则
│   ├── classification_rules/ ← 分类规则
│   ├── category_knowledge/   ← 类目知识
│   ├── keyword_rules/     ← 关键词规则
│   ├── listing_rules/     ← Listing规则
│   ├── source_rules/      ← 来源规则
│   └── prompt_templates/  ← 提示词模板
├── REJECTED/              ← 驳回知识
├── OUTDATED/              ← 过期知识
├── CASES/                 ← 案例库
│   ├── success/           ← 成功案例
│   └── failure/           ← 失败案例
├── REVIEW_QUEUE/          ← 审查队列
└── templates/             ← 模板文件
```

## 自生长流程

1. **识别** — 每次 Hermes 完成任务后，识别本次新经验
2. **写入** — 按知识卡片格式写入 `PENDING/`
3. **验证** — Data Verifier 验证来源和真实性
4. **审核** — Commander 审核通过后移到 `VERIFIED/`
5. **驳回** — 不通过移到 `REJECTED/`
6. **过期** — 过期移到 `OUTDATED/`
7. **更新** — 更新 `INDEX.md` 和 `CHANGELOG.md`

## 知识卡片格式

每条知识必须是独立 Markdown 文件，带 YAML frontmatter：

```yaml
---
id:            # 唯一ID (KB-分类-序号)
title:         # 知识标题
type:          # knowledge | case | rule | template
category:      # 所属分类
tags:          # 标签列表
roles:         # 适用角色
status:        # pending | verified | rejected | outdated
confidence:    # A(多方验证) | B(来源可靠) | C(交叉验证中) | D(单来源) | E(待验证)
source:        # 数据来源
evidence:      # 证据链接
created_at:    # 创建时间
updated_at:    # 更新时间
reviewed_by:   # 审核人
expires_at:    # 过期时间 (可选)
related:       # 关联知识ID
supersedes:    # 取代哪个旧知识
superseded_by: # 被哪个新知识取代
---
```

## 与 Obsidian 集成

本仓库可直接作为 Obsidian Vault 打开：
- `[[wikilinks]]` 双向链接 → Graph View 知识图谱
- YAML frontmatter → Dataview 结构化查询
- `templates/` → Obsidian 模板

```bash
# 在 Obsidian 中打开
open vault → 选择 hermes-knowledge-base 目录
```

## Hermes 集成

Hermes Agent 通过 GitHub MCP 读写本仓库：
- 任务完成 → 自动写入 `PENDING/`
- 定期审核 → PENDING → VERIFIED / REJECTED
- Skill 更新 → 同步到 `SYSTEM_RULES/`

## License

MIT