---
id: SYS-006
title: 中文化规则
type: rule（规则）
category: system_rules（系统规则）
tags: [中文化, 交付, 字段, 模板]
roles: [Commander, Product Analyst, Market Researcher, Keyword Specialist, Listing Writer, data-analyst, Data Verifier]
status: verified（已验证）
confidence: A（用户制定）
source: 威猛先生制定
evidence: 2026-08-22 亲自部署
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: Commander
---

# 中文化规则

## 结论

所有交付给威猛先生的内容必须中文优先。技术目录/程序识别用英文保留，正文/规则/表格/审查结果全部中文化。

---

## 一、保留英文的部分

以下技术目录/字段保留英文：
- README.md, INDEX.md, CHANGELOG.md（文件名）
- SYSTEM_RULES, PENDING, VERIFIED, REJECTED, OUTDATED（目录名）
- REVIEW_QUEUE, CASES, RAW, templates（目录名）
- id, status, source, evidence, related, commit（字段ID）
- repo（仓库）, branch（分支）, pull request（合并请求）, issue（任务/问题）

---

## 二、必须汉化的部分

1. 文档标题
2. 正文内容
3. 字段说明
4. 规则说明
5. 知识卡片内容
6. 表格表头
7. 索引说明
8. changelog 内容
9. review 内容
10. commander 审核结果
11. Data Verifier 验证结果
12. 交付说明

---

## 三、状态字段中英文对照

所有状态写成：
- pending（待审核）
- verified（已验证）
- rejected（已拒绝）
- outdated（已过期）
- case-only（仅限案例）
- draft（草稿）

---

## 四、可信等级中英文对照

- A（官方/用户文件/多次验证）
- B（Amazon/卖家精灵/截图支撑）
- C（单次项目验证）
- D（待验证经验）
- E（已否决或过期）

---

## 五、知识卡片模板（中文版）

```yaml
---
id: KB-XXX-001
title: 中文标题
type: 中文类型
category: 中文类目
tags: 中文标签
roles: 中文角色
status: pending（待审核）
confidence: A/B/C/D/E
source: 中文来源
evidence: 中文证据
created_at: 2026-08-22
updated_at: 2026-08-22
reviewed_by: 未审核
expires_at: 2027-02-22
related: 相关知识
supersedes: 替代旧知识
superseded_by: 被新知识替代
---
```

---

## 六、INDEX.md 索引表头

```
ID | 标题 | 类型 | 类目 | 状态 | 可信等级 | 标签 | 摘要 | 更新时间 | 文件路径
```

---

## 七、CHANGELOG.md 更新日志格式

```
日期：
任务名称：
新增内容：
修改内容：
废弃内容：
审核结果：
提交记录：
```

---

## 八、技术词首次出现必须加解释

例如：
- commit（提交记录）
- repo（仓库）
- branch（分支）
- pull request（合并请求）
- issue（任务/问题）
- pending（待审核）
- verified（已验证）

---

## 关联知识

- [[SYS-005]] 省Token自成长机制
- [[SYS-001]] 最高铁律