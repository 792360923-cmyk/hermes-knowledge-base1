# PENDING（待审核区）— 待审核知识

> 所有新识别的经验先写入此目录，经 Data Verifier 验证 + Commander 审核后才能移入正式规则库。

## 历史复盘入库（2026-08-22）— 10批共44条

| ID | 标题 | 批次 | 类型 | 状态 |
|----|------|------|------|------|
| KB-ANTI-FAKE-001 | 禁止编造数据——宁Unknown不硬填 | 1 | 规则 | pending（待审核） |
| KB-ANTI-FAKE-002 | 来源标注规则——每个关键字段必须标注来源 | 1 | 规则 | pending（待审核） |
| KB-ANTI-FAKE-003 | 未标注≠无——区分未标注和无 | 1 | 规则 | pending（待审核） |
| KB-SOURCE-001 | 数据来源优先级——Amazon参数表第一 | 2 | 规则 | pending（待审核） |
| KB-SOURCE-002 | 卖家精灵Coupon列——%和$两种格式须正确换算 | 2 | 规则 | pending（待审核） |
| KB-SOURCE-003 | Alexa来源标注——可信度低于listing正文 | 2 | 规则 | pending（待审核） |
| KB-SOURCE-004 | 卖家精灵详细参数列——Key:value格式的结构化金矿 | 2 | 规则 | pending（待审核） |
| KB-SOURCE-005 | BSR和销量——大类/小类/父体/子体不能混用 | 2 | 规则 | pending（待审核） |
| KB-CLASSIFY-001 | 产品分类必须按物理形态——不按营销词 | 3 | 规则 | pending（待审核） |
| KB-CLASSIFY-002 | 子代理分类错误——手动误判电动/漏无刷电机/合并三层分类 | 3 | 规则 | pending（待审核） |
| KB-CLASSIFY-003 | 智能眼镜三层细分——运动/日常+AI+摄像 | 3 | 规则 | pending（待审核） |
| KB-CLASSIFY-004 | 配件不能当整机——套装必须判断是否含主机 | 3 | 规则 | pending（待审核） |
| KB-CLASSIFY-005 | 图片与标题冲突——优先信图片，标记待核实 | 3 | 规则 | pending（待审核） |
| KB-FIELD-001 | 充电方式必须细分到具体接口——禁止只写USB | 4 | 规则 | pending（待审核） |
| KB-FIELD-002 | 电池字段细分——锂电池/铅酸/干电池/纽扣/未标注 | 4 | 规则 | pending（待审核） |
| KB-FIELD-003 | 遥控/控制方式细分——遥控器/APP/蓝牙/WiFi/触控/按键 | 4 | 规则 | pending（待审核） |
| KB-FIELD-004 | 防水字段细分——IPX4/IPX5/IPX6/IPX7/IP67/未标注 | 4 | 规则 | pending（待审核） |
| KB-FIELD-005 | 所有字段必须量化——不能笼统写"容量大""功率高" | 4 | 规则 | pending（待审核） |
| KB-TABLE-001 | Excel交付格式——主图嵌入+中文标题+三层分类底色 | 5 | 规则 | pending（待审核） |
| KB-TABLE-002 | 单位统一——重量g/kg、容量ml/L/mAh、价格USD | 5 | 规则 | pending（待审核） |
| KB-TABLE-003 | 结论必须有数据+占比+原因+影响+建议 | 5 | 规则 | pending（待审核） |
| KB-TABLE-004 | 空值和异常值必须标注——不能直接跳过 | 5 | 规则 | pending（待审核） |
| KB-TABLE-005 | 辅助列必加——中文标题100条完整翻译+竞对列 | 5 | 规则 | pending（待审核） |
| KB-REVIEW-001 | Commander逐页验收——每页必须单独通过才能进下一页 | 6 | 规则 | pending（待审核） |
| KB-REVIEW-002 | 总指挥复查9项指标——任何一项不通过=需返工 | 6 | 规则 | pending（待审核） |
| KB-REVIEW-003 | delegate_task子代理——关键步骤不委托Commander亲自做 | 6 | 规则 | pending（待审核） |
| KB-REVIEW-004 | 交付前自查——不能把草稿当最终稿 | 6 | 规则 | pending（待审核） |
| KB-REVIEW-005 | Data Verifier验证——所有数据提交前必须验证 | 6 | 规则 | pending（待审核） |
| KB-CATEGORY-GARMENT-001 | 挂烫机——10条形态规则+保护功能核对 | 7 | 知识 | pending（待审核） |
| KB-CATEGORY-BIKE-001 | Bike Pumps——电动/手动分类+无刷电机溢价规律 | 7 | 知识 | pending（待审核） |
| KB-CATEGORY-BLOWER-001 | 吹叶机——5类型+CFM定价+差评TOP5 | 7 | 知识 | pending（待审核） |
| KB-CATEGORY-GLASSES-001 | 智能眼镜——三层细分+萌芽功能识别 | 7 | 知识 | pending（待审核） |
| KB-CATEGORY-GEN-001 | BSR调研通用流程——卖家精灵导出全覆盖 | 7 | 知识 | pending（待审核） |
| KB-KB-001 | 知识库四级读取模式——默认只注常驻短规则 | 8 | 规则 | pending（待审核） |
| KB-KB-002 | PENDING不能自动升级正式规则库——等用户审核 | 8 | 规则 | pending（待审核） |
| KB-KB-003 | 任务末尾自动输出知识库增量建议 | 8 | 规则 | pending（待审核） |
| KB-KB-004 | 错误黑名单格式——每犯错生成短规则 | 8 | 规则 | pending（待审核） |
| KB-KB-005 | 中文化交付——状态中英对照+技术词首次解释 | 8 | 规则 | pending（待审核） |
| KB-FAIL-001 | 子代理Coupon换算错误——20%off当成减$20 | 9 | 案例 | pending（待审核） |
| KB-FAIL-002 | 子代理三层分类合并——产品类型/外观/场景合为一列 | 9 | 案例 | pending（待审核） |
| KB-FAIL-003 | Commander重新分类引入新错误——放弃重写用修正 | 9 | 案例 | pending（待审核） |
| KB-FAIL-004 | Discord发.xlsx收不到——必须.zip打包 | 9 | 案例 | pending（待审核） |
| KB-SUCCESS-001 | 吹叶机差评驱动差异化——Tavily+第三方交叉验证法 | 10 | 案例 | pending（待审核） |
| KB-SUCCESS-002 | 智能眼镜市场演进四阶段法——萌芽/成长/成熟/标配 | 10 | 案例 | pending（待审核） |

**类型统计**：规则30条 / 知识5条 / 案例8条 / 失败案例4条 / 成功案例2条

## 审核流程

1. Hermes 任务完成 → 识别新经验
2. 按 `templates/knowledge_card_template.md` 格式写入
3. Data Verifier 验证来源
4. Commander 审核
5. 通过 → 正式规则库 | 驳回 → 已拒绝区