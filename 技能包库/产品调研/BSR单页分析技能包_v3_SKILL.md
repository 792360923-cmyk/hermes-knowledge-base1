---
name: bsr-single-page-analysis
description: BSR100单页分析：Excel含冻结筛选/中文标题/分类/竞品标色/结论。触发：BSR/第二页/单页分析/替换表带。
version: 1.0.0
---

# BSR单页分析技能包 v1.0

> 一页Excel完成BSR TOP100全量分析。输入：卖家精灵导出的BSR前100 Excel + 目标ASIN + 类目链接。
> 输出：单Sheet Excel，含表头冻结筛选、中文标题、类目专属细分字段、竞品颜色标记、底部结论区。

## 前置条件
1. 用户提供卖家精灵导出的 `BSR{类目名}Current-100-US-{日期}.xlsx`
2. 用户提供目标 ASIN 及类目链接
3. 汇率当天查：`curl -s "https://api.exchangerate-api.com/v4/latest/USD" | python3 -c "import sys,json; d=json.load(sys.stdin); print(f'{d[\"rates\"][\"CNY\"]:.2f}')"`

## 执行流程（7步）

### Step 1: 数据加载 + 目标产品确认
- Pandas `read_excel` 读BSR前100 (engine='openpyxl')
- 目标ASIN用 `asin_detail` 拉详情
- 确定竞品范围（同设备/同材质/同适配的才标颜色，不相关的白底）

### Step 2: 类目定制分类维度
从标题+卖点+参数穷举所有维度，不同类目→不同细分列。

**通用列**：
`#`,`图`,`中文标题`,`品牌`,`适配设备/大类`,`材质细分`,`外观类型`,`扣环/连接方式`,
`价格$`,`Prime$`,`Coupon`,`评分`,`评数`,`上架`,`ASIN`,`链接`,`月销`,`月销$`,`月销¥`,
`包装数`,`佩戴/安装方式`,`防水/防护`,`宽度/规格`,`品牌类型`,`AC`,`BSeller`,`变体`,`天数`,`LQS`,
`FBA`,`运费$`,`A+`,`视频`,`卖点(中文)`

**类目专属列**：
- 表带类：适配设备,材质细分(16种),外观类型(10种),扣环(7种),佩戴位置,防水
- 烟熏器类：材质,充电方式,LED灯,显示屏,安全盖,风扇,木屑数,冷烟,含喷枪,过滤嘴
- 调酒器类：件数,材质,颜色,支架类型,摇酒器类型,捣棒,量杯,过滤器,配方卡

### Step 3: 中文标题
格式 `[设备/类型] 品牌 材质+外观 特征`
表带：`[Whoop5.0] omee 硅胶蕾丝镂空 2件装`

### Step 4: 中文卖点
英文→中文短词逗号分隔。映射：soft→柔软, breathable→透气, stretchy→弹力, waterproof→防水, sweatproof→防汗, washable→可水洗, quick-dry→速干, easy install→易安装, magnetic→磁吸, lace→蕾丝镂空, floral→花纹雕刻

### Step 5: 颜色标记
- 🔴 红底 #FFC7CE = 目标ASIN
- 🔵 蓝底 #BDD7EE = 高相关竞品
- ⬜ 白底 = 不相关

### Step 6: Excel格式化
- R1标题13pt Bold #1F4E79浅灰底 | R2概览9pt Bold | R3表头8pt Bold黑字浅黄底
- 表头冻结 A4，自动筛选 A3:XX103
- 图片55×55嵌入，行高55px

### Step 7: 底部结论区（5模块）
1. 市场结构（材质/适配/外观/扣环分布+数据）
2. 市场演变（年份×功能渗透率时间轴+明年预判）
3. 竞品对标（目标赛道6-8个TOP竞品逐一分析）
4. 切入建议（3方向+定价+配置+理由+不做清单）
5. 兼容性Q&A（跨代/跨机型核实，如适用）
结论格式：🥇绿底 | ❌红底 | ✅最终决策绿字绿底

## 完整Python模板（通用版，支持3类目）

调用 `skill_view('bsr-single-page-analysis', file_path='assets/template.py')` 获取完整可执行模板。
模板通过 `CATEGORY_TYPE` 变量切换类目：

| CATEGORY_TYPE | 类目 | 自定义列 |
|---|---|---|
| `"bands"` | 替换表带 | 适配设备, 材质16细分, 外观10种, 扣环7种, 佩戴位置, 防水 |
| `"smoker"` | 威士忌烟熏器 | 类型(电动/火枪), 材质, 充电方式, LED, 显示屏, 安全盖, 风扇, 木屑, 冷烟, 喷枪, 过滤嘴, 礼盒 |
| `"shaker"` | 鸡尾酒调酒器 | 类型(套装/冰石/单品), 件数, 材质, 颜色, 支架, 摇酒器类型, 捣棒, 量杯, 过滤器, 配方卡, 礼盒, 便携包 |

改5个变量即可跑：`EXCEL_PATH / CATEGORY_TYPE / TARGET_ASIN / TARGET_VALUE / CATEGORY_NAME`

## 输出与检查
- ✅ 表头冻结+筛选 | ✅ 仅竞品有颜色 | ✅ 中文标题+卖点
- ✅ 分类细分到最小粒度 | ✅ 结论含具体数字 | ✅ 兼容性Q&A已核实