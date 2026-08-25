---
技能包名称：亚马逊Alexa购物助手核对技能包
分类：亚马逊运营
版本：v1
状态：待审核
创建日期：2026-08-25
更新日期：2026-08-25
适用场景：用Alexa/Rufus核对产品参数
来源：历史经验/Hermes技能包
是否当前推荐：否
上一版本：无
下一版本：无
维护人：Hermes小助理
审核人：未审核
文件路径：技能包库/亚马逊运营/亚马逊Alexa购物助手核对技能包_v1.md
---

---
name: amazon-alexa-rufus-query
description: 用亚马逊AI购物助手(Alexa/Rufus)核对产品参数。登录→Open Alexa panel→问参数。
---

# 亚马逊 AI 购物助手（Alexa/Rufus）问答核对参数

## 用途
当产品标题/五点/参数表里没有某个字段（夜灯有无、亮度调节、静音dB、覆盖面积等），用亚马逊产品页的 AI 购物助手（Alexa/Rufus）提问核对。用户口中的"alex"就是它。

## 前提
- Alexa/Rufus 面板**只在登录态出现**，未登录时按钮不渲染（DOM 里没有 alexa/rufus 元素）。
- 用用户亚马逊买家号登录（Lisa 792360923@qq.com / Feiye123）。
- 用 browser_navigate（隐身浏览器），不要用 Playwright（headless 被 block）。

## 流程（已验证可用）

1. **登录**：`browser_navigate` 到 `https://www.amazon.com/ap/signin`，输入邮箱 → Continue → 密码 → Sign in。若弹"Keep hackers out"绑手机号页，点「Not now」跳过。
2. **进产品页**：`browser_navigate` 到 `/dp/{ASIN}`。
3. **点开面板**：左上角导航栏「All」菜单右侧的蓝色「**Open Alexa panel**」按钮（snapshot 里 ref 对应文字 "Open Alexa panel"，点开后变成 "Close Rufus panel"）。
4. **输入问题**：面板是左侧抽屉，输入框是 `<textarea id="rufus-text-area" placeholder="Ask a shopping question">`。用 browser_console 的 React 原生 setter 赋值（否则 React 不认）：
   ```js
   var ta=document.getElementById('rufus-text-area');
   var setter=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,'value').set;
   setter.call(ta,'你的英文问题');
   ta.dispatchEvent(new Event('input',{bubbles:true}));
   ```
5. **提交**：`document.getElementById('rufus-submit-button').click()`（aria-label="Submit"）。
6. **读回答**：`document.querySelector('.rufus-conversation-container')` 或 `.rufus-conversation-papyrus-container` 的 innerText，含 "Customer question" + 回答全文。

## 关键要点 / 坑

- **问题用英文问**（listing 是英文，AI 用英文答更准）。
- **预设问题按钮更省事**：面板里有现成 pill 按钮（"Can I customize the mood lights?"/"How large is the coverage area?"/"What mist settings are available?" 等），`[class*="rufus-pill"]`，直接 click 即可，不用打字。
- **Alexa 只复述 listing 内容，不会无中生有**：listing 没写的字段（如亮度调节具体档位、精确dB），Alexa 也会说 "product details don't explicitly specify..."——这时字段仍标「未标注」，不能把 Alexa 的推测当事实。
- **反爬风险**：点开面板后若页面变 about:blank 或登出，重新登录再来一次。登录态 + Rufus SPA + 反爬叠加偶发不稳定，多试一次通常能成。
- **面板渲染时序**：点开「Open Alexa panel」后按钮变「Close Rufus panel」即面板已开，但内容可能稍后才进 DOM，`#rufus-text-area` 可能需等 1-2 秒再查。

## 和 amazon-browser-lookup / amazon-browser-scraping 的关系
- 抓标题/五点/参数表用那两个 skill（browser_navigate + browser_console）。
- 标题五点里缺的字段，用本 skill 问 Alexa 二次核对。
- 三者数据源：卖家精灵(Excel) / 产品页抓取 / Alexa问答 / 识图，按需组合，来源字段要在表里标注。

