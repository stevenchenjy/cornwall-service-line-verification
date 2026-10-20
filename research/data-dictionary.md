# Field mapping - documentary support, local confirmation pending

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

On October 20, 2026, the official Health Data NY attached dictionary (August 2024, physical page 2) and NYSDOH guidance v3 (August 2025, physical page 8, Figure 3-A) were retrieved, text-read and visually inspected. They support the material/method distinction and the headings used above. Metadata connects the API identifiers to those headings; the PDF dictionary itself does not print the API identifiers. See the [source review](../reports/official-guidance-review.md), [page-level evidence table](official-source-evidence.csv) and [retrieval manifest](../data/manifests/official-guidance-intake.json).

The interpretation is `documentary_supported_local_confirmation_pending`. The current API descriptions still discuss historical lead under `current_public_side_sl`, method under `was_public_sl_material_ever`, installation date under `public_sl_material`, and diameter under `public_sl_installation_or`. Retain those original descriptions in `data/schema/inventory-fields.json`; do not silently rewrite source metadata. The dictionary instead defines these as current material, historical lead status, verification method, and installation/replacement date, respectively. This does not authenticate individual rows or confirm Cornwall's local acceptance rules.

Keep historical public-side lead status distinct from current material and retain its supporting evidence. Guidance v3 physical pages 7 and 9 make upstream history and segment extent relevant to interpretation; public/customer column names do not by themselves establish ownership in every system. Confirm the local segment and ownership mapping.

`rowsUpdatedAt` is a dataset-level timestamp, not an update date for Cornwall or any individual line. Do not infer a missing PWS ID from locality.

Derived labels are `unknown`, `missing`, `reported_known` and `unmapped`. Preserve raw values. Reported-known means a material name exists in the record; it does not independently establish physical verification or regulatory acceptance.

Conservative address/ZIP keys can miss spelling and abbreviation variants. Stable departmental line IDs and a restricted crosswalk are required for identity. The attempt contract now distinguishes submission, evidence review, classification accept/reject/defer and correction history; final acceptance requires a validated documentary bundle.
