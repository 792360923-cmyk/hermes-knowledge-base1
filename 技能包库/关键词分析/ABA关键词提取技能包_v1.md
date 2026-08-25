---
技能包名称：ABA关键词提取技能包
分类：关键词分析
版本：v1
状态：待审核
创建日期：2026-08-25
更新日期：2026-08-25
适用场景：amz123提取ABA热搜词数据
来源：历史经验/Hermes技能包
是否当前推荐：否
上一版本：无
下一版本：无
维护人：Hermes小助理
审核人：未审核
文件路径：技能包库/关键词分析/ABA关键词提取技能包_v1.md
---

---
name: amz123-aba-extraction
description: Extract ABA data from amz123 via browser. Never use curl.
---

# amz123 ABA 热搜词数据提取

## 核心教训

**curl 正则提取不可靠！** amz123 页面数据通过客户端 JS 渲染，curl 只抓到内嵌 JSON 部分，会丢失 50%+ 衍生词。

**实测对比（2026-07）：**

| 主语词 | curl | 浏览器 | 丢失率 |
|--------|------|--------|--------|
| star projector | 5 条 | 12 条 | 58% |
| night light projector | 9 条 | 11 条 | 18% |
| galaxy projector | 7 条 | 8 条 | 13% |

## 正确方法

### 1. 导航

```
browser_navigate → https://www.amz123.com/usatopkeywords?k=KEYWORD
```

逐个主语词执行，不可批量。

### 2. 提取排名数字 — 优先 innerText 法（TreeWalker 会误抓杂号）

TreeWalker 遍历 `main` 会把 ICP 备案号、客服电话、导航数字等页面杂号全抓进来（实测 "steamer for clothes" 抓出 50 个数字导致对齐错乱），且 `document.querySelector('main')` 偶尔返回 null（页面偶发跳到 about:blank）。**优先用 body.innerText 切片法：**

```javascript
const txt = document.body.innerText;
const idx = txt.indexOf('搜索词');   // 表格区域起点
const tableText = txt.slice(idx, idx + 1000);
return { tableText };
```

返回的 tableText 结构：跳过两行重复表头「搜索词/本周排名/上周排名/涨跌幅度」后，每 4 行一组 = (关键词, 本周排名, 上周排名, 涨跌幅度)。注意：上周排名可能为 0（新词无上周数据）；涨跌幅度 = |本周-上周| 绝对值。若 `idx` 返回 -1 说明页面未渲染完成 → 重新 `browser_navigate` 该 URL 再试。

### 2b. TreeWalker 备用法（innerText 不可用时）

```javascript
const main = document.querySelector('main');
const nums = [];
const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
while(walker.nextNode()) {
  const v = walker.currentNode.textContent.trim();
  if (/^\d+$/.test(v) && parseInt(v) > 10) nums.push(parseInt(v));
}
// nums 每 3 个一组 → (本周排名, 上周排名, 涨跌)
```

### 3. 提取关键词

从 browser_snapshot 的 LayoutTable 区域读链接文本。过滤导航链接（排名/全部/搜索词/国家名/涨跌幅度/首页等）。

### 4. 组装

关键词列表[N] → nums[N*3], nums[N*3+1], nums[N*3+2]

## 示例

`galaxy projector` → "8个搜索结果"：

| 关键词 | 本周 | 上周 | 涨跌 |
|--------|------|------|------|
| galaxy projector | 3,635 | 2,822 | +813 |
| galaxy projector night light | 9,506 | 7,609 | +1,897 |
| astronaut galaxy projector | 20,865 | 21,672 | -807 |

## 反模式

```bash
# ❌ curl 丢失客户端渲染数据
curl -s "https://www.amz123.com/usatopkeywords?k=..." | grep...
# ❌ fetch 被 CORS 拦截
fetch("https://www.amz123.com/usatopkeywords?k=...")
```
