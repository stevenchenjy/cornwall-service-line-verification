# Official New York guidance and field-semantics review

Reviewed October 20, 2026 (America/New_York). Scope: primary-source verification for intake, not a regulatory determination or Cornwall acceptance policy. Review was performed inline by the AI session preparing this handoff. No independent reviewer or person has verified these sources for this project.

## Sources actually retrieved and read

The previously blocked guidance URL returned HTTP 200 when requested with a browser user agent. The alternate official host returned the identical PDF SHA256. The web browsing fetch still returned 403 for the main URL; that failure did not prevent local byte retrieval. The downloaded document identifies itself as **LCRR v3, August 2025**, with 15 physical pages. This is the version retrieved, not a claim that no later instruction or system-specific condition exists.

| Source ID | Official source and issue date | Inspection completed |
|---|---|---|
| `nys-guidance-main-retry` | [NYSDOH inventory guidance](https://www.health.ny.gov/environmental/water/drinking/docs/service_line_inventory_guidance_lcrr.pdf), August 2025 v3 | Text extracted for all 15 pages; visual inspection of physical pages 1, 5, 7-12 |
| `nys-lsli-data-dictionary` | [Health Data NY attached dictionary](https://health.data.ny.gov/api/views/j63k-4n92/files/5e17b5f4-794c-4627-a7af-60c6dc181bb0?download=true&filename=NYSDOH_LSLI_Data_Dictionary.pdf), August 2024 | All four pages text-read; physical pages 1-3 visually inspected |
| `nys-lsli-overview` | [Health Data NY attached overview](https://health.data.ny.gov/api/views/j63k-4n92/files/26df4877-4aec-4f75-87b7-6fa690e91ad6?download=true&filename=NYSDOH_LSLI_Overview.pdf), August 2024 | Both pages text-read and visually inspected |
| `nys-inventory-metadata-intake` | [Current public API metadata](https://health.data.ny.gov/api/views/j63k-4n92.json), retrieved October 20, 2026 | Field names, display headings, descriptions and attachment identifiers compared with the pinned metadata and saved schema |
| `nys-pws-inventory-directory` | [NYSDOH system inventory directory](https://www.health.ny.gov/environmental/water/drinking/service_line/), retrieved October 20, 2026 | Cornwall-named entries and system-specific link text-read |
| `nys-pws-ny3503526-page` | [Village of Cornwall-on-Hudson system summary](https://www.health.ny.gov/environmental/water/drinking/service_line/NY3503526.htm), retrieved October 20, 2026 | System-information, aggregate inventory and certification sections text-read; table-cell alignment checked |

Exact retrieval timestamps, URLs, hashes, byte lengths and ignored local paths are in [the access manifest](../data/manifests/official-guidance-intake.json) and [retrieval ledger](../data/manifests/retrievals.csv). The [evidence table](../research/official-source-evidence.csv) records the issue period, physical PDF page, unit, calculation and inspection status per finding. AI text-and-visual inspection is labeled `ai_text_and_visual_checked`; it is not `human_verified`. These administrative sources are authoritative for what NYSDOH published, not empirical effectiveness studies; journal/retraction grading is inapplicable. No independent corroboration of local implementation is claimed.

## Findings for the intake contract

| Evidence ID | Documentary finding | Intake consequence |
|---|---|---|
| NY-G01 | v3 p. 1 distinguishes unknown status from identified material. | Preserve Unknown, missing and unmapped values separately. |
| NY-G02 | v3 pp. 7-8 distinguish historical lead, current material, method and category. | Obtain all four; preserve a category as reported until its decision evidence is reviewed. |
| NY-G03 | v3 p. 9 uses main-to-curb and curb-to-building segments even when ownership differs. | Ask for segment limits and ownership separately. |
| NY-G04 | v3 p. 10 calls for cross-checking records and physical confirmation when confidence is inadequate. | Request the corroborating evidence and unresolved conflicts. |
| NY-G05 | v3 p. 12 combines resident identification with qualifying staff verification; unclear photos need another reliable method. | Log submission and assessment separately. |
| NY-G06 | v3 pp. 1, 7 make upstream history relevant to GSLRR. | Request historical public-side lead evidence. |
| NY-G07 | v3 p. 11 treats predictive acceptance case by case. | Request any applicable approval; infer none. |
| NY-G08 | v3 p. 11 conditions the post-ban route on written whole-system and full customer-line construction records. | Building age alone supplies no acceptance decision. |

These are bounded readings of a dated guidance document. They do not establish which procedures Cornwall currently accepts, whether any record satisfies them, or whether a state-approved model exists locally. No numerical physical-verification threshold is imported as a local success probability.

## Field mapping now has documentary support

The attached dictionary, physical page 2, supports the meanings below. Its printed headings match the API display names; the API identifiers are obtained from metadata, not printed in that PDF. Guidance Figure 3-A on physical page 8 also presents the material/history/method columns. These documents share the same institutional publisher; agreement is not independent-source validation. The raw metadata and saved schema remain unchanged.

| API identifier | Supported interpretation | API-description issue retained |
|---|---|---|
| `locality` | Geographic locality | Does not identify the water system |
| `current_public_side_sl` | Current public-segment material | API description instead discusses historical lead |
| `was_public_sl_material_ever` | Previous public-segment lead status | API description instead discusses method |
| `public_sl_material` | Public-segment verification method | API description instead discusses installation date |
| `public_sl_installation_or` | Public-segment installation/replacement date | API description instead discusses diameter |
| `public_sl_size` | Public-segment diameter | No conflict found in the reviewed definition |
| `customer_sl_material` | Customer-segment material | No conflict found in the reviewed definition |
| `customer_sl_material_1` | Customer-segment verification method | No conflict found in the reviewed definition |
| `sl_category` | Reported overall inventory category | Category definitions are on dictionary physical page 3 |

The interpretation is **documentary-supported; local export confirmation pending**. This resolves the earlier reliance on headings and observed values alone. It does not repair the state API, establish local identity/freshness, authenticate filed categories, or convert historical method frequencies into attempts. The overview's physical page 2 describes submitted inventory information and annual updates; it does not date individual records. The dictionary's summary fields include system identity, but that does not supply a PWS-to-row crosswalk for this locality extract.

## Dated system summary: an identity lead, not a replacement baseline

The official directory links Cornwall-on-Hudson to **NY3503526**. The linked summary's Section I names the **Village of Cornwall-on-Hudson** and that PWS ID. Section III reports **2,553 total service lines** and **1,514 Unknown service lines** in its aggregate two-cell rows. Section V displays certification date **`10/15/24`**, interpreted as October 15, 2024; no individual-row observation dates are supplied. The page's footer revision date is not substituted for the certification or inventory observation date. These are reported summary counts, not a verified current population.

Evidence IDs NY-S00-NY-S04 pin the directory, summary labels, source date and values. Their scope and date differ from the archived locality extract of 1,110 raw rows / 808 Unknown. Do not subtract these totals to infer omitted lines, compute a trend, assign the locality rows to this PWS, or replace the allocation baseline. The useful next question is whether NY3503526 is the intended study system and how a current dated stable-ID export reconciles both sources, including other localities. No row identities have been confirmed.

## Next evidence gate

Use the [intake handoff](../research/intake-handoff.md) for dated identity, crosswalk, historical material and attempt coverage. The workflow engine checks documentary consistency under supplied rules; it does not implement the full NYSDOH classification rules. In particular, the existing side-material patterns do not themselves establish historical upstream conditions. Those conditions need authorized substantive review before an applicable rule/decision is validated. All eight empirical readiness gates remain unconfirmed, and the independent review checklist remains pending.

AI assistance was used for retrieval, text extraction, visual inspection and preparation of this report. Original PDFs and renders remain local and ignored; only receipts and authored findings are eligible for public review.
