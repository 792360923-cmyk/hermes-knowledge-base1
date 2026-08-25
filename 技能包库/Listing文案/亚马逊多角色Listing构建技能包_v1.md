---
技能包名称：亚马逊多角色Listing构建技能包
分类：Listing文案
版本：v1
状态：待审核
创建日期：2026-08-25
更新日期：2026-08-25
适用场景：多角色自动委派构建Listing
来源：历史经验/Hermes技能包
是否当前推荐：否
上一版本：无
下一版本：无
维护人：Hermes小助理
审核人：未审核
文件路径：技能包库/Listing文案/亚马逊多角色Listing构建技能包_v1.md
---

---
name: amazon-multi-role-listing
description: "Build Amazon Listing with multi-role auto delegation."
version: 1.0.0
---

# 亚马逊多角色 Listing 构建

## 执行纪律

1. **严格按 amazon-listing-builder 8步顺序**，不可跳步
2. **Step 5（卖点结构）和 Step 6（中文卖点）完成后必须暂停等用户确认**
3. **品牌/参数来源必须是 Amazon 页面实际抓取，不推测**
4. **图片URL必须从 Amazon DOM 提取并升级为 AC_SL1500**
5. **AI评论摘要从页面对客户可见的 cr-summarization-ai 区域提取**

## 多角色自动分派模式

当用户指令包含"listing/链接/卖点/文案"时，自动分派：

| 角色 | 任务 | 时机 |
|------|------|------|
| 产品分析师 | 爬取竞品Listing数据 | Step 1（并行） |
| 市场调研员 | 卖点频率统计+消费者洞察 | Step 2-3 |
| 关键词专家 | 关键词整合+PPC策略 | Step 6-7 输入 |
| 数据验证师 | QC+合规检查 | Step 4 |

### 竞品爬取分派规则

- 每次 delegate_task 最多 5 个 ASIN 给一个子代理
- 3个子代理并行覆盖 15 个竞品
- 每个子代理提取：`productTitle / bylineInfo / price / rating / reviews / feature-bullets / wayfinding-breadcrumbs / images(AC_SL1500) / BSR / AI评论摘要(cr-summarization-ai) / 评分分布(histogramTable)`

## Amazon 登录 OTP 处理

当需要登录买家号提取不公开数据时：
1. `browser_navigate` → `https://www.amazon.com/gp/sign-in.html`
2. 输入邮箱 → 输入密码
3. 遇到验证码页面时**立刻请求用户提供邮箱验证码**
4. 收到验证码后**快速输入提交**（页面可能超时过期）
5. 登录成功后立即导航到目标ASIN页面提取数据
6. 如果验证码过期，重新走完整登录流程（不跳过步骤）

## 常见问题

- **BSR字段不可用**：新版Listing模板可能不展示BSR，标记为"页面未展示"不编造
- **AI评论摘要无数据**：评论量少（<1000）可能未生成AI摘要，标记为"评论量不足"
- **技术参数未渲染**：动态加载的表格需要滚动触发，或用browser_console执行scrollTo
- **"Continue shopping"拦截**：点击按钮通过后重新navigate到同一URL
- **验证码页面过期**：重新走完整流程（邮箱→密码→验证码），不跳过步骤

## 输出格式

最终Excel必须包含7个Sheet + 总结页：
英文文件名发送，竞品标题/品牌不出现任何竞品品牌名。

