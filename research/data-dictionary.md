# Field mapping — provisional semantic review

| API field | Display label / analysis use |
|---|---|
| locality | Service Line Locality；地理字段，不是 PWS 编号 |
| street_address / zip_code | 本地候选匹配键；不能当唯一管线 ID |
| current_public_side_sl | Current Public Side SL Material；公共部分原始材料标签 |
| customer_sl_material | Customer SL Material；住户部分原始材料标签 |
| public_sl_material | Public SL Material Verification Method；公共部分确认方法，不是材料本身 |
| customer_sl_material_1 | Customer SL Material Verification Method；住户部分确认方法 |
| sl_category | 原始整条分类；Unknown / Non-Lead / GSLRR 等原值保留 |
| location | 精确地理点，只在本地，外部结果只用审核后的汇总 |
| note | 原始备注可能含标识信息，不发布 |

字段映射以数据集当前 display name 和实际内容作为预检依据，仍需部门确认。当前 metadata 部分 public-side description 有疑似错位，不作为唯一语义依据。
rowsUpdatedAt 是整个数据集更新时刻，不是 Cornwall 或每条管线的更新时间。没有公开 PWS 字段不代表可据 locality 补出该字段。

标准化标签：`unknown` / `missing` / `reported_known` / `unmapped`。保留原始值；known 表示原记录有材料名称，并不额外保证现场验证或法规认可。
