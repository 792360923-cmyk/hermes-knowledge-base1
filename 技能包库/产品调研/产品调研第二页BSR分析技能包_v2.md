---
name: product-analysis-page2
description: 亚马逊BSR第二页功能与数据分析（通用，适用所有产品类目）。
version: 2.0.0
---

# 第2页 — BSR前100功能与数据分析（通用版）

调研任何产品类目的 BSR 前100，做功能/参数/差异化分析，输出带图片、中文标题、结论分析、市场概览的 Excel。适用于所有产品类目（香薰机/黄油盘/小家电/3C/工具/家居等）。

## 数据来源（4个，按需组合）
1. **卖家精灵产品查询导出**：含 ASIN/标题/品牌/大类BSR/价格/评分/评分数/上架时间/FBA运费/配送/月销量/月销售额/详细参数/产品卖点/A+页面/视频/主图。卖家精灵字段（月销/月销售额/FBA运费/大类排名/上架时间）只有卖家精灵能给，未提供时留空禁止编造。**详细参数列必须逐项解析**：`Key: value | Key: value` 格式，每个Key都是候选列（Brand/Material/Connector Type/Battery Capacity/Operating System/Memory Storage Capacity等），不能只解析两三个就跳过去。
2. **Amazon 产品页抓取**：用 browser_navigate（隐身浏览器，非Playwright）逐个进产品页抓标题(#productTitle)/五点(#feature-bullets)/品牌(#bylineInfo)/价格/评分/评论数/参数表(#productOverview_feature_div/#productDetails_techSpec_section_1)。参数表要**逐行读取所有Key**（含充电方式Connector Type、蓝牙版本、电池类型、存储容量等结构化字段）。反爬"Continue shopping"拦截时：点Continue→重新导航同一/dp/URL。
3. **Alexa 购物助手问答核对**：五点+参数表里没有的参数（夜灯/亮度调节/静音dB/覆盖面积/充电方式/防抖轴数等）用 Alexa 问（见 `amazon-alexa-rufus-query` skill：登录Lisa→Open Alexa panel→#rufus-text-area输入→#rufus-submit-button提交→读回答）。Alexa只复述listing，listing没写的它也答不出，仍标"未标注"。
4. **图片识别补充**：参数表+五点都没有、但信息图/A+图里画了的参数（防水等级/续航/充电方式/镜片类型/接口），用 browser_get_images 取副图→curl下载→image_analysis识别。信息图是功能参数的最全来源，标题/五点经常省略。

## 营销/运营维度（卖家精灵导出必带）
价格/Prime价格/Coupon/月销量/月销售额/子体销量/大类BSR/小类BSR/BSR增长率/评分/评分数/月新增评分数/留评率/Q&A数/上架时间/上架天数/配送方式(FBA-FBM-AMZ)/配送时长/FBA运费/卖家数/Buybox卖家/卖家所属地/Best Seller标识/Amazon's Choice/New Release/CPF绿标/A+页面/视频介绍/品牌故事/SP广告/秒杀/变体数。这些是卖家精灵一键导出就有的，不要漏填。

## 固定板块（17列，始终包含）
小类排名序号、图片(70×70嵌入)、中文标题、链接(可点击Amazon产品页)、品牌、大类目排名、价格、Coupon、评分、评论数、上架年份时间、ASIN、FBA运费、配送渠道(FBA/FBM)、月销量、月销售额美金、月销售额RMB、竞品类型

## 功能卖点分级着色（表格设计铁律）

**底色规则（极简，禁止花哨）**：
- 普通数据行：**白色底**（不用任何颜色）
- 竞对行：红底 #FFC7CE 加粗
- 机械按压/配件行：浅黄底 #FFEB9C（异常/差评产品警示）
- **禁止**：不同类型用不同底色（密封胶蓝/托盘黄/离型纸橙等），眼花缭乱

**核心功能卖点列着色规则**（整列统一按最高优先级着色）：
- 🔴 **红色** = 差异化核心功能（竞品少/独特卖点）：真空吸附、LED灯、免蜡、金属笔尖、螺纹设计、快干喷雾、联锁拼接、童话设计、GRS环保
- 🔵 **蓝色** = 成本/售价相关功能（影响采购成本或定价）：无线、可充电、多档吸力、Type-C充电
- 🟢 **绿色** = 客户在意功能（影响购买决策但不贵）：静音、人体工学、轻量、防溢、带盖、双面、不粘、无毒、快干、亮度可调、收纳
- 普通功能 = 黑色（或无特殊色）

**英文标题处理**：
- **不在表格里放英文标题列**（太占宽度）
- 英文标题只在后台数据解析时使用，中文标题逐条完整翻译显示

## 可选板块（不同分析项目，用户勾选）
完整字段库见 `references/category-fields.md`（通用字段约70个 + 17类目约750个字段）。
用法：先扫类目统计各字段在竞对中的出现频率，高频字段=类目判断标准=必列维度+假想产品必做功能，低频=可选差异化；再按类目让用户勾选进表。

### 字段穷举铁律（所有类目适用，禁止偷懒）
1. **先穷举，再选字段**：拿到前100标题 + 竞对五点/参数后，必须逐条扫描，把标题/五点/参数里**每一个出现的卖点/参数都提取出来**，每个独立卖点对应一列，禁止只从字段库挑"印象里的常见字段"。
2. **禁止合并细分维度**：能细分的一律拆开，常见漏项：
   - 防抖 → 必须拆「防抖类型」(6轴EIS/普通EIS/Anti-Shake/无) + 是否标注轴数；
   - 降噪 → 必须拆「麦克风数量」(双麦/单麦/无) + 「降噪类型」(Dual-Mic ENC/ENC/ANC/普通/无)；
   - AI助手 → 必须拆具体产品名(ChatGPT-4o/ChatGPT/Gemini/Meta AI/语音助手/无)；
   - 像素/分辨率 → 必须拆具体数值(8MP/12MP/13MP/32MP、4K/3K/1200P/1080P)；
   - 翻译 → 必须拆「是否支持翻译」+「语言数」(164+/139/138/100+等)；
   - 续航 → 必须拆「播放时长(h)」+「电池续航(h)」；
   - 蓝牙 → 必须拆具体版本号(5.4/5.3/5.0/未标)。
3. **遗漏判断法**：对着标题逐字读，问"这个卖点有没有独立一列承载？"——例如标题写 `Dual-Mic ENC Noise Cancelling`，就必须有"麦克风数量"列 + "降噪类型"列；写 `Privacy Cover` 必须有"隐私盖"列；写 `WiFi Transfer` 必须有"WiFi传输"列；写 `Meeting Transcription` 必须有"会议转录"列。
4. **分类优先于堆列**：同一物理维度（如镜片）拆成多个细分列（镜片类型/多镜片配件/防蓝光/UV400/安全认证）比塞进一个"备注"列更利于对比。
5. **字段库是字典不是清单**：字段库列的是"可选维度候选"，不是"本次必用字段"。每个类目调研前先扫标题穷举，字段库里没有的新卖点要当场补充进表并回写字段库。

### 竞对专项验证（每次必须，禁止跳过）
竞对产品不能用正则匹配标题/五点就完事。必须单独进入Amazon详情页逐项核对：

## ⚠️ 产品主分类核实铁律（电动/手动/机械按压必须逐ASIN问Alexa）

凡是产品主分类涉及以下判断时，**禁止靠标题关键词硬判**，必须逐 ASIN 问 Alexa 核实：
- 电动 / 手动
- 机械按压 / 电池驱动
- 整机 / 配件 / 耗材 / 套装
- 自动 / 手动

**坑**：标题含 `automatic` / `dispenser` / `press` / `bead blitz` 等词 ≠ 电动。这些是营销词，实际可能是机械手动按压（手按出钻）。必须以是否有 `battery` / `electric` / `motor` / `usb rechargeable` / `type-c` / `vacuum` / `mAh` 等**电源证据**为准。

Alexa 必问："For ASIN [ASIN], is this product electric powered, battery powered, motorized, or a manual/mechanical press operated by hand? Does it have a motor, battery, or USB charging?"

分类规则：
- 有 battery/electric/motor/USB 明确证据 → 电动
- Alexa 说 manual/mechanical/hand press/non-electric → 手动或机械手动按压
- 只有 automatic/dispenser/press 词、无电源证据 → 不能归电动，核实后定类或"待核实"
- Alexa 无法确认 → "待核实"，禁止硬判

失败案例：B0HC72TVK4（Bead Blitz Automatic Dispenser）等6个产品标题含"automatic"，实为机械手动按压（无电机无电池无USB），分类错误率38%。详见知识库 KB-FAIL-005。

1. **详情页抓取**：browser_navigate到竞对/dp/页面，读取 `#productOverview_feature_div` 参数表（含Connector Type/充电方式等）、`#feature-bullets` 五点、`#aplus_feature_div` A+
   - `#productOverview_feature_div` 或 `#productDetails_techSpec_section_1` 参数表（含Connector Type/充电方式/蓝牙版本等结构化数据）
   - `#feature-bullets` 五点卖点
   - `#aplus_feature_div` A+内容
2. **图片识别补充**：browser_get_images取副图信息图，curl下载后用image_analysis识别（信息图里常含Title/五点没写的参数如防水等级/续航/充电方式）
3. **Alexa核对**：五点+参数表都没有的字段，登录Lisa账号→Open Alexa panel→问，标"Alexa来源"

**⚠️ 电动/带电类竞品必须逐ASIN问Alexa核实专属字段**（KB-FAIL-006教训）：
凡是涉及电机/电池/充电的产品，以下字段五点+参数表经常不写，必须问Alexa：
- 电机转速(RPM)：问 "what is the motor speed in RPM?"
- 电池容量(mAh)：问 "what is the battery capacity in mAh?"
- 充电接口：问 "what charging port does it use, Type-C or Micro USB?"
- 防水等级：问 "is it waterproof, and what IPX rating?"
- 续航时间：问 "how long does the battery last per charge?"
Alexa 答不出来的 → 填"未标注（Alexa无法确认）"，注明"Alexa来源"
**禁止**：电动竞品的电机/电池/充电/防水字段直接留空——这是偷懒，必须问过Alexa后才填
4. **验证对比**：竞对提取结果 vs Amazon详情页实际数据，不一致用Amazon数据覆盖
5. **记录差异**：如果正则提取的结果和详情页不一致，说明正则有问题，要修正全局提取逻辑

### 提取后自检清单（发表格前必须逐项过）
- [ ] 充电方式是否区分了**Type-C有线 / 磁吸充电 / 充电盒 / 触点充电 / Micro USB**？不能只写"USB"
- [ ] 外观造型/镜框形态是否每种都有独立的列？是否从标题/图片穷举了所有造型？
- [ ] 竞对的**每一个字段**都是Amazon详情页验证过的，不是纯正则匹配？
- [ ] 有没有"未标"但实际产品页面信息图里有、Alexa能答出来的字段？
- [ ] `product_type.value_counts()` 最大类占比 < 50%？（超过50%说明分类太粗）
- [ ] **兜底类（"通用"/"其他"等）占比 < 10%？**
- [ ] 所有数值型字段（像素/分辨率/防抖轴数/电池容量mAh/存储容量GB）都拆成了具体数值？
- [ ] 「详细参数」列里的 Connector Type、Connectivity Technology 等结构化字段全部解析了？
- [ ] **中文标题100条无空白？卖家精灵翻译为空时已fallback生成？**
- [ ] **关键词提取用了词边界（`\b`）而非子串匹配？没有"light"误判"lightweight"？**
- [ ] **电动/带电竞品的电机/电池/充电/防水字段已逐ASIN问过Alexa？**

## 表头/格式规范

| 元素 | 设置 |
|------|------|
| 标题行 | 微软雅黑 13pt Bold #1F4E79 居中，合并整行 |
| 表头行 | 浅黄底 #FFFFCC，微软雅黑 9pt Bold 黑字 |
| 结论行(R3) | 浅绿底 #E2EFDA，合并整行，9pt #1F4E79，自动换行 |
| 市场概览行(R4) | 浅灰底 #F0F0F0，10pt 粗体，合并整行 |
| 数据行 | 微软雅黑 9pt/8pt，行高70-75px |
| 竞对行 | 红底 #FFC7CE 加粗（仅3-5个竞品） |
| 机械按压/差评行 | 浅黄底 #FFEB9C（警示色，非装饰色） |
| 普通数据行 | **白色底**（禁止按产品类型分色，眼花缭乱） |
| 功能/差异化卖点列 | 按层级着色：红字(#FF0000)=差异化核心 | 蓝字(#0066CC)=成本相关 | 绿字(#006600)=客户在意 | 普通功能无特殊色 |
| 图片 | 70×70px 缩略图嵌入图片列 |
| 链接列 | Amazon产品页URL，可点击超链接 |

## 中文标题生成
从英文标题+详细参数+产品卖点提取关键词组合：品牌+材质+核心功能+规格。
写法："{品牌} {材质/核心功能} {规格参数} {兼容/场景}"。必须逐条完整翻译英文标题的含义，禁止公式拼凑。

**⚠️ 中文标题必须有 fallback 生成逻辑**：卖家精灵"标题(翻译)"字段为空时，不能留空！必须按以下公式逐条生成：
- 公式："{品牌} + {核心功能/刷头结构} + {主词} + {材质} + {规格}"
- 例：GRILLART 无刷毛 烧烤刷 带刮刀 不锈钢手柄 18英寸
- 例：Leebein 电动旋转 烧烤刷 3档调速 5000mAh
- 例：Webber 烧烤清洁剂喷雾 除油 16盎司
- **100条不允许任何空白**，卖家精灵翻译为空时必须自动生成

材质英文映射：Ceramic→陶瓷, Plastic→塑料, Stainless Steel→不锈钢, Aluminum→铝合金, Alloy Steel→合金钢, Silicone→硅胶, Bamboo→竹子, Wood→木头, Acrylic→亚克力, Brass→黄铜, Nylon→尼龙, Carbon Fiber→碳纤维, Kevlar→凯夫拉

## 多层分类方法论（所有类目适用）
产品分类不能一个维度一刀切。必须**三层拆解**：

### 第一层：功能形态（有没有核心部件）
判断优先级：配件(无完整主体)→有摄像头(AI相机眼镜)→有AI助手但无摄像头(AI眼镜，核心卖点是ChatGPT/语音助手/智能问答)→有实时翻译但无摄像头(翻译眼镜)→有蓝牙音频(音频眼镜)→纯物理(墨镜/防晕动)→其他。
**陷阱**：有AI助手的眼镜不能因为也有翻译或音频就归入翻译眼镜/音频眼镜——它的购买决策驱动是"AI智能"，不是"翻译"或"音乐"。分类看核心卖点，不看附属功能。

### 第二层：外观造型（长什么样，影响用户认知）
从标题/图片/参数中提取镜框/机身/外壳的造型特征，必须穷举所有出现的造型并独立成列：
- 智能眼镜：Wayfarer / Headliner / Skyler / Aviator / 运动款 / 圆形 / 方形 / 飞行员款
- 小家电：立式 / 桌面式 / 壁挂式 / 手持式 / 便携式
- 工具类：枪式 / 直柄式 / 折叠式 / 伸缩式

**陷阱**：不要把"外观造型"合并到"产品类型"里。类型是功能层，造型是视觉层——Wayfarer AI相机眼镜 ≠ 运动款AI相机眼镜，功能和价位完全不同。

### 第三层：使用场景（在哪用，影响购买决策）
从标题/五点/图片提取使用场景，一个产品可以有多个场景：
- 智能眼镜：骑行/徒步/Vlog/办公/驾驶/旅行/会议
- 小家电：卧室/客厅/厨房/办公室/旅行

### 分类自检
- `clean['产品类型'].value_counts()` 数量最多的类是否超过50%？超过说明分类太粗，需要第二层拆分
- **兜底类（"通用"/"其他"/"烧烤刷(通用)"等）占比必须 < 10%**，超过10%必须拆解
- 是否至少有一种外观造型形成独立的一列？
- 竞对的外观造型是否和它同价位竞品一致？（不一致说明分类有误）

**⚠️ 场景词 ≠ 类型词**：五点里的 "for cast iron"（适用于铸铁）是**使用场景**，不是产品类型！只有标题明确写 "Cast Iron Brush" 才归入铸铁类型。类似坑："for porcelain grates"→场景、"for weber"→品牌适配、"for stainless steel"→材质场景，都不能当产品主分类。场景词归入"使用场景"列（第三层），不当类型（第一层）。失败案例：Grill Brushes 调研把五点里 "for cast iron" 误判成"铸铁清洁刷"类型，10件假分类。详见 KB-FAIL-006。

## 功能/卖点提取（通用方法）
从产品卖点(英文)提取核心功能，用✅前缀，最多7项。常见映射：airtight→密封, one-hand→单手, dishwasher→洗碗机, microwave→可微波, magnetic→磁吸, water seal→水封, brushless→无刷电机, one-touch→一键, bpa-free→BPA-free, non-slip→防滑, transparent→透明, rechargeable→可充电, cordless→无线, waterless→无水, app control→APP控制, remote→遥控, timer→定时, auto shut-off→自动关机, night light→夜灯, ambient light→氛围灯, whisper-quiet/quiet→静音。功能卖点列红字加粗（差异化关键）。

**⚠️ 关键词提取必须用词边界，禁止子串匹配**：
- ❌ `'light' in text` → 会匹配 "lightweight"、"light-weight"、"FlexTexture" 的子串，误判"轻量"为"LED灯"
- ✅ `re.search(r'\bled light\b', text)` 或精确词组 `"led light" / "built-in light" / "illuminat"`
- ❌ `'led' in text` → 会匹配 "tangled"、"installed"、"disabled"
- ✅ `re.search(r'\bled\b', text)` 并排除 "tangled"/"installed" 等
- ❌ `'ce ' in text` → 会匹配 "piece"、"once"、"price"
- ✅ 用精确词组而非子串，CE/FCC等认证从Product Overview字段提取而非全文搜
- 失败案例：Grill Brushes 调研中 `('light','LED灯')` 把 Scrub Daddy 误判为带LED灯。详见 KB-FAIL-006。

## 结论分析（5段 + 做/不做决策）
1. **款式/类型分布**：各类型数量+占比，主流类型及卖得好的原因。
2. **售价因素**：影响价格的核心参数（材质/容量/功能/认证/电机类型等）。
3. **市场演变趋势**（必须分析，不能跳过）：
   - 按上架年份分组（2020前/2020/2021/2022/2023/2024/2025/2026），统计每个年份上架产品数量
   - 选出5-8个核心功能维度（如：摄像头像素/视频分辨率/防抖类型/降噪/充电方式/AI助手/防水），逐个画出时间线：
     - 2022年：都是XXX
     - 2023年：开始出现XXX
     - 2024年：XXX渗透率到X%
     - 2025年：出现XXX（最新趋势）
     - 2026年：XXX（新动向）
   - 结论格式示例："2023年前类目全是蓝牙音频眼镜($20-40)，2024年出现8MP AI相机眼镜($50-70)，2025年集中爆发4K+EIS($60-90)，2026年出现6轴EIS+双麦ENC($100+)——目前不到5个产品有这个组合，是切入窗口"
   - 判断每个功能的演变阶段：萌芽期(渗透率<10%)→成长期(10-30%)→成熟期(30-60%)→标配期(>60%)
4. **配件/功能**：标配配件 + 差异化卖点列举，竞对缺失项。
5. **切入方向**：建议做什么方向（定价+核心配置+差异化）+ 不做原因（红海/垄断/无利润）。切入方向必须结合演变趋势——选"萌芽期"的功能做差异化、避开"标配期"的红海。
结尾必须明确"**做/不做**"决策。

## 市场概览（R4）
总计X产品 | 总月销量X | 总月销售额$X | 品牌数X | 均价$X | A+覆盖率X% | 视频覆盖率X%

## 汇率规则（强制）
月销售额RMB 必须用**当日实时汇率**换算，禁止用固定汇率（如7.2）。
- 每次做表前先查当日 USD/CNY 汇率（tavily_search 搜 "USD to CNY exchange rate today"，取 XE/OFX 中间价，精确到小数点后2位）。
- 表格标题或概览行标注"汇率：1 USD = X.XX CNY (YYYY-MM-DD)"。
- 如果同一天做多张表，共用同一个汇率值。

## 技术细节
- **主图下载**：从BSR页或产品页提取主图ID（`#landingImage` src 的 `images/I/{ID}`），用 `curl https://m.media-amazon.com/images/I/{ID}._AC_UL320_.jpg` 下载，openpyxl 嵌入 70×70。图片ID含`+`号的文件名须去`+`。
- **品牌提取**：`#bylineInfo` 的 textContent，`replace('Visit the ','').replace(' Store','').trim()`，禁止从标题推断。
- **BSR列表提取**：`[data-asin]` 选择器，filter asin.length==10，标题/评分/价格在同元素内。

## 验证标准
- 产品全量抓取（前100或用户指定范围）
- 中文标题逐条翻译
- 结论4段 + 市场概览
- 色标正确（竞对红底/类型分色/功能红字）
- 图片嵌入
- 卖家精灵字段未采集时留空，禁止编造
- 改完直接发表格给用户（Discord 用 MEDIA 发 .zip），不要只口头说"已更新"
