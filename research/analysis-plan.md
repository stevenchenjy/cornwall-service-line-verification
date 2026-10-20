# Analysis plan — draft, before substantive research

1. 保存 j63k-4n92 元数据和完整限定 locality 查询快照；保留请求、抓取时间、SHA256、数据集级 rowsUpdatedAt 与抓取前后计数。两次计数不同或元数据变更则重新抓取。
2. 校验所需机器字段并查看实际取值分布。2026-10-19 元数据中部分 public-side 描述似乎与显示字段错位；不要仅依描述推断含义。用原始列名、内容和部门确认共同解决，记录未解决的映射。
3. 不修改原始值。派生标签以 Unicode/空格/大小写规则处理：explicit Unknown（含 Unknown but could be lead）、missing、reported known 和 unmapped 分开。Known Other 只是原台账报告已知，不等于现场证据足够。
4. 只在原 `sl_category=Unknown` 原始记录内统计公共/住户双侧缺口；同时检查非 Unknown 类别与单侧信息是否矛盾。575/176/57 等数字仅是待复现的预研基线。
5. 报告地址+ZIP 完全相同和谨慎标准化后的重复键组数、涉及行数、超额行数；不自动合并公寓、单位或相邻门牌。重复键不证明同一管线或历史版本。人工队列仅保存在 data/restricted/。
6. 分别记录 resident-only、public-records-only、field-public、field-customer、joint-field 等行动的目标桶、尝试工时、联系率、证据被接受概率、联合成功率与复查成本。未取得校准数据前，所有率都是情景假设。
7. 双侧 Unknown 完整解决须两个部分都得到可接受证据。联合概率不可未经声明地用边际概率乘积替代。居民自查单独能直接补齐整条记录的初始上限，仅针对 public-reported-known/customer-unknown 桶且仍需证据审核。
8. 比较同预算的完整解决数、完整解决/工时或成本、单侧改进、仍缺公共侧的数量和分配公平性。对疑似重复的原始行基线与经部门确认的独立管线基线分别报告。
9. 不提前宣布唯一最优政策。用参数区间和敏感性找出改变策略排序的阈值；在部门确认字段、边界和成本后再做推荐。
10. 独立 reviewer 复核边界、重复规则、证据质量、失败与重试、概率相关性和披露。成果披露 AI 协助和记录未更新/未去重的局限。
