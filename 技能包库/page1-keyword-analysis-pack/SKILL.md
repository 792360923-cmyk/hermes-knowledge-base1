---
name: page1-keyword-analysis-pack
description: 第一页关键词分析 FINAL。改CONFIG即生成6板块+趋势图Excel。全站点适用。
version: 5.0.0-FINAL
self_contained: true
keywords: [amazon, 第一页, 关键词, page1, 趋势图, excel, 6板块]
requirements:
  - openpyxl
  - 卖家精灵 MCP (asin_detail, traffic_keyword, keyword_miner, keyword_research_trends)
---

# 第一页关键词分析 独立技能包 v4.0

> **自包含技能包**。加载本技能 → 读数据获取流程 → 改 CONFIG → 运行模板脚本 → 输出 Excel。
> 不依赖任何本地 KB 路径，任何 Agent 环境可直接使用。

---

## 核心概念

**输出**: 1个 Excel 文件，2个 Sheet
- Sheet「第一页关键词分析」: 6个板块从上到下
- Sheet「趋势图表」: 4线折线图 + 55月原始数据

**6个板块**:

| # | 板块名 | 颜色 | Hex |
|---|--------|------|-----|
| 1 | 关键词对比数据表(8词) | 浅蓝 | #D5E4F7 |
| 2 | 核心对比分析(6维x5词+蓝海判定) | 浅绿 | #E2EFDA |
| 3 | 三阶段切入策略 | 浅绿 | #E2EFDA |
| 4 | 5条详细结论(数据/分析/操作/预期四段) | 浅黄 | #FFF2CC |
| 5 | 数据来源说明 | 浅红 | #FCE4D6 |
| 6 | 两年趋势分析(同比收窄+定性) | 浅蓝 | #D5E4F7 |

---

## 数据获取流程 (卖家精灵 MCP)

```
Step 1: asin_detail(marketplace, asin)
        → 产品名/价格/BSR/评分/变体数/上架日期/FBA

Step 2: traffic_keyword(asin, marketplace, order_by=searches, size=30)
        → 该 ASIN 真实流量词 Top30

Step 3: keyword_miner × 3-5次 (并行, 每次一个核心词)
        → keyword, searches, purchases, purchaseRate,
          bid, bidMin, bidMax, products, supplyDemandRatio,
          spr, monopolyClickRate, cvsShareRate, searchRank,
          titleDensity, relevancy

Step 4: keyword_research_trends × 4-5次 (并行, 每次一个核心词)
        → 55个月 search + yearlyGrowth 数据
        ⚠️ 这个 API 不用 request 包装，直接传顶层参数:
        {"keyword": "xxx", "marketplace": "US"}
```

### 关键词筛选逻辑

从 traffic_keyword + keyword_miner 交叉选取 8 个关键词:

| 优先级 | 选取标准 | 数量 |
|--------|---------|------|
| 🔴主推 | 精准核心词, 需供比>10, 商品<1000 | 2个 |
| 🔴次推 | 长尾变体, SPR<20 | 1-2个 |
| 🟡辅助 | 相邻品类词, 低价拓流 | 2个 |
| ⚠️观察 | 偏泛但搜索量大, 谨慎投放 | 1-2个 |
| ⚠️避免 | 大类词/跨品类混淆词 | 1个 |

### 蓝海判定标准

同时满足: 需供比>20 + 商品数<500 + SPR<15 + PPC<$0.40
(注: 酒类等小众品目 PPC 普遍偏高, 蓝海判定可放宽 PPC 条件)

---

## 颜色规范

| 场景 | 字体 | 填充 |
|------|------|------|
| 标题行 | Arial 14pt Bold #FFFFFF | #1F4E79 |
| 板块标题 | Arial 12pt Bold #1F4E79 | D5E4F7/E2EFDA/FFF2CC/FCE4D6 |
| 表头 | Arial 10pt Bold #FFFFFF | #1F4E79 |
| 主推行(🔴) | Arial 10pt | #FCE4D6(浅红) |
| 辅助行(🟡) | Arial 10pt | #FFF2CC(浅黄) |
| 正文 | Arial 10pt | 无 |
| 小注 | Arial 9pt | 无 |
| 产品信息条 | Arial 9pt #666666 | 无 |

---

## 趋势分析规范

### 定性三阶段
1. **爆发期**: 搜索量峰值最大 + yearlyGrowth > 0
2. **回调期**: yearlyGrowth 首次 < 0 的月份开始
3. **企稳期**: 最近6个月同比跌幅收窄

### 同比收窄判断
- 跌幅从 50%→10%: 企稳 ✅
- 跌幅从 50%→60%: 仍在跌 ❌
- 已转正增长: 恢复 ✅

### 市场定性速查

| 搜索量 | 需供比 | 定性 |
|--------|--------|------|
| 年增>20% | >30 | 上升蓝海 |
| 稳定 | >20 | 成熟蓝海 |
| 暴跌后企稳 | >20 | 回调后稳定 |
| 年减>20% | 任意 | 衰退中 |

---

## 板块具体字段定义

### 板块1: 关键词对比数据
优先级 / 关键词 / 月搜索量 / ABA排名 / PPC($) / 购买率 / 需供比 / 商品数 / SPR / 推荐度

### 板块2: 核心对比分析
月搜索量 / 需供比 / PPC / SPR / 商品数 / CVR → 每行5词 + 结论列

### 板块3: 三阶段切入策略
阶段 / 目标 / 主推词 / 月搜索 / PPC预算 / 打法 / 预期排名 / 出单占比

### 板块4: 结论 (每条4段式)
【数据】【分析】【操作】【预期】各≥1句

### 板块5: 数据来源
项目 / 数据来源 / 说明 (8行)

### 板块6: 趋势分析
趋势总结表(4词) + 同比收窄表 + 长文本分析 + 市场定性

---

## 质量自检清单

- [ ] 6板块完整 + 趋势图表Sheet存在
- [ ] 颜色区分正确 (红=主推, 黄=辅助)
- [ ] 结论每条4段式 (数据/分析/操作/预期)
- [ ] 所有数字有来源标注
- [ ] 无「可能」「大概」「估计」
- [ ] 趋势有三阶段定性 + 收窄数据 + 市场定性
- [ ] 蓝海判定标准已写
- [ ] xlsx → zip → Discord 发送

---

## 常见错误

| 错误 | 原因 | 修复 |
|------|------|------|
| `keyword_research_trends` missing required | 用了request包装 | 直接传顶层 marketplace + keyword |
| `TypeError: expected Fill` | fills[i]=None | 判空: if fills and fills[i] is not None |
| `SyntaxError: 1,180` | 千分位逗号→tuple | 整数不写逗号: 1180 |
| Discord 收不到 xlsx | 限制 | zip 打包, 不行换短英文名 |

---

## 使用方式

### 方式一: 手动填充 CONFIG

1. 按「数据获取流程」调用卖家精灵 MCP 收集数据
2. 打开 `templates/generate.py`
3. 改 CONFIG 区 5 个部分:
   - `MARKET`, `ASIN`, `CURRENCY`
   - `PRODUCT` 字典
   - `KEYWORDS` 列表 (8词 × 10字段)
   - `TRENDS` 字典 (4-5词 × 55月)
   - 板块2 comps / 板块3 strats / 板块4 concs / 板块6 trends 文字结论
4. 运行: `python3 templates/generate.py`
5. 输出: `/tmp/{ASIN}_{MARKET}_第一页.xlsx`

### 方式二: 让 Agent 全自动执行

```
Agent 加载本技能 → 调卖家精灵 MCP → 
提取数据 → 写 CONFIG → 运行脚本 → 输出 Excel
```

**Agent 执行注意事项**:
- keyword_research_trends 直接传顶层参数，不用 request 包装
- 数据填充后运行脚本，不要在 Agent 内部手动构建 openpyxl
- 所有数据来自 MCP，禁止编造
- 板块4结论必须每条约100字(4段)，不可缩写