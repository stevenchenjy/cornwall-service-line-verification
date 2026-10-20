# Field mapping — provisional semantic review

| API field | Display label / analysis use |
|---|---|
| locality | Service Line Locality; geographic location, not a PWS ID |
| street_address / zip_code | Local candidate matching key; not a unique service-line identifier |
| current_public_side_sl | Current Public Side SL Material; original public-side material label |
| customer_sl_material | Customer SL Material; original customer-side material label |
| public_sl_material | Public SL Material Verification Method; evidence method, not the material itself |
| customer_sl_material_1 | Customer SL Material Verification Method; customer-side evidence method |
| sl_category | Original complete-line category; preserve Unknown, Non-Lead, GSLRR and other original values |
| location | Precise geographic point; local-only; external outputs require reviewed aggregation |
| note | Original notes may contain identifying information; do not publish |

The provisional mapping uses current display labels and observed content and still requires departmental confirmation. Several public-side metadata descriptions appear misaligned; do not rely on those descriptions alone.

`rowsUpdatedAt` is a dataset-level timestamp, not an update date for Cornwall or any individual line. Do not infer a missing PWS ID from locality.

Derived labels are `unknown`, `missing`, `reported_known` and `unmapped`. Preserve raw values. Reported-known means a material name exists in the record; it does not independently establish physical verification or regulatory acceptance.
