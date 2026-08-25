---
id: KB-KW-001
title: 亚马逊关键词研究全流程技能 — amazon-keyword-research 技能包
type: knowledge
category: 关键词规则
tags: [关键词研究, ABA扩词, 否定词, 前台搜索, 主语词, 卖家精灵, Amazon]
roles: [Commander, 词研, 所有角色]
status: pending
confidence: A
source: 严宇坤提供的技能包 zip 文件，经6个产品案例验证
evidence: 技能包内含6个case study (nail glue/castor oil/ingrown toenail/rear bike rack/foldable travel steamer/galaxy projector)
created_at: 2026-08-25
related: [KB-ANTI-FAKE-001, KB-ANTI-LAZY-003, KB-FIELD-006]
---

# 亚马逊关键词研究全流程技能

## 规则结论

`amazon-keyword-research` 是集成技能，将7步关键词研究流程固化为一键式执行规范。从竞品ASIN发现→卖家精灵反查→ABA扩词→否定词提取→前台搜索→Excel输出，全部自动化。禁止跳过任何步骤或自行编造关键词。

## 规则详情

### 工具依赖
- **oathtool** (已安装 2.6.11)：2FA OTP 自动生成
- **openpyxl** (已安装 3.1.5)：生成 7 Sheet Excel
- **amazon-scraper** (VPS 无 Docker，降级为浏览器模式)
- **卖家精灵 asinsight**：用户本地导出 Excel 提供
- **amz123.com**：ABA 数据源（curl 直接提取，非浏览器）

### 7步执行流程

| Step | 名称 | 关键输入 | 关键输出 | 确认点 |
|------|------|---------|---------|--------|
| 0 | 信息收集 | 对标ASIN/类目/买家账号/卖家精灵方式/ABA站点 | 5项齐全 | 用户确认 |
| 1 | 类目发现 | ASIN→BSR榜单→同类ASIN | 同类ASIN清单(50+) | 用户确认同类 |
| 2 | 反查词频 | 卖家精灵反查→合并去重→拆主语词/修饰词 | 主语词统计+修饰词统计 | 用户确认主语词 |
| 3 | ABA扩词 | 主语词→amz123搜索→衍生词 | ABA扩词表(含翻译) | 自动 |
| 4 | 否定词 | 4轮提取：品牌/主语/修饰/词意 | 否定词表+有效词清单 | 自动 |
| 5 | 前台搜索 | XHR批量搜索(50词/批)→分类器评级 | 同款/接近/不确定/不同款 | 自动 |
| 6 | Excel输出 | 7 Sheet固定顺序 | 最终关键词研究.xlsx | 用户验收 |

## 禁止

- ⛔ 禁止跳过 Step 0：必须集齐对标ASIN/类目/买家账号/卖家精灵方式/ABA站点5项后才能开始
- ⛔ 禁止自行编造关键词：Step 5 搜索词必须来自 Sheet 2 卖家精灵数据
- ⛔ 禁止自行判断同类型：BSR 同类判断必须用户确认
- ⛔ 禁止拆开主语词：如 "nail glue" 是完整词根，不能拆成 "nail"+"glue"
- ⛔ 禁止品牌词粗暴匹配：不能用2个字母匹配（如"dr"误杀"dress"）
- ⛔ 禁止跨对话复用：每个产品必须新对话，不去翻历史聊天记录
- ⛔ 禁止跳步或减少 Sheet 数量（固定7个Sheet）

## 适用场景

- 亚马逊美国站及多站点关键词研究
- 竞品关键词反查与分析
- Listing 优化关键词布局
- PPC 广告关键词筛选
- 否定关键词精准投放

## 来源证据

技能包由严宇坤提供，已通过 6 个产品案例验证：
1. Nail Glue（美甲胶）
2. Castor Oil Roller（蓖麻油滚珠）
3. Ingrown Toenail Corrector（嵌甲矫正器）
4. Rear Bike Rack（自行车后货架）
5. Foldable Travel Steamer（折叠旅行蒸汽机）
6. Galaxy Projector Night Light（星空投影灯）

## 安装记录

- 安装路径：`~/.hermes/skills/amazon-keyword-research/`
- 包含：SKILL.md（482行）+ 14个 reference 文件（案例/工具/算法）
- 依赖：oathtool ✅ / openpyxl ✅ / amazon-scraper ❌（VPS无Docker，降级浏览器）