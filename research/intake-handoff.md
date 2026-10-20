# Baseline, operations and independent-review handoff

Prepared October 20, 2026. This packet can be reviewed without running a model. No request has been sent and no departmental export, local rule, real decision bundle or independent human review has been received. Empty templates contain headers only; complete them in ignored `data/restricted/`, never in the public seed directory. Existing department formats may be mapped instead.

## 1. Dated identity and baseline

Use the [baseline header](../data/seed/service-line-baseline-template.csv) for one current record per department-confirmed `(pws_id, case_id)` at an agreed `baseline_as_of`. Preserve earlier versions in original exports. A baseline date is the inventory cut-off; `line_record_as_of` is the row's documented observation/update date and may be null. Do not substitute the API dataset timestamp for either.

Public identity lead: the official state directory and [system summary](https://www.health.ny.gov/environmental/water/drinking/service_line/NY3503526.htm) associate Village of Cornwall-on-Hudson with NY3503526. The [source review](../reports/official-guidance-review.md) preserves the summary's reported totals and `10/15/24` certification separately. Confirm that this is the intended study system and obtain its current boundary/unique-line export. This public lead does not assign the 1,110 locality rows to a system or date them.

| Field group | Required interpretation / missingness |
|---|---|
| `pws_id`, `case_id`, `baseline_as_of` | Authoritative system and stable pseudonymous line identity plus dated population. Missing identity prevents admission to an allocation population. |
| `source_inventory_ref`, `source_row_id` | Restricted received-export reference and source row locator. Pin the export's bytes, SHA256, receipt time, reporting period and permissions in the intake record. |
| `inventory_scope_status` | Proposed values: `in_scope`, `out_of_scope`, `unresolved`; obtain boundary and inclusion rules, including relevant other localities. Never remove unresolved rows from the audit denominator silently. |
| `reported_public_material`, `reported_customer_material`, `public_method_reported`, `customer_method_reported` | Original values, not accepted-evidence flags. Retain blank, explicit Unknown and unrecognized labels distinctly in the mapping ledger. |
| `public_previously_lead_reported`, `historical_public_evidence_ref` | Preserve the original historical status and documentary support, including unresolved history. This is needed for review of galvanized-line categories. |
| `public_evidence_status`, `customer_evidence_status`, side evidence references | `unreviewed`, `submitted`, `accepted` or `rejected` as supported by actual records. A historical method label cannot populate `accepted`. The engine's side state does not replace historical upstream facts. |
| `reported_category`, `accepted_category`, `decision_ref`, `acceptance_rule_ref`, `decision_date` | Separate a filed category from a substantively reviewed accepted decision. Retain the source's reported acceptance in the original export if documentary validation is incomplete; leave curated acceptance pending. |
| `record_validation_status` | `pending`, `validated` or `excluded_with_reason`, with the reviewer and reason in the restricted validation record. Structural completeness alone is not validation. |

Use the [crosswalk header](../data/seed/inventory-crosswalk-template.csv) to relate pinned public source rows to the baseline. `source_export_sha256` plus a 1-based `source_row_1based` is a snapshot locator, never a line ID. Preserve the 1,110 public raw rows and all 43 repeated address/ZIP groups. A same-address pair is only a candidate; differently spelled addresses may also be candidates.

Record `relationship` as a proposed interpretation (`same_line`, `distinct_line`, `revision`, `unmatched_public`, `department_only`, `unresolved`) and `match_status` as `pending` or `confirmed`. Confirmation requires authoritative identity evidence, reviewer and date. Maintain both rows if identity is unresolved. Permit multiple source rows per confirmed line and record department-only lines; never force one-to-one matching. Any exclusion needs an explicit reason. Reconcile source-row coverage, unmatched records and department-only coverage before reporting a unique-line total. No crosswalk has been populated or records merged here.

## 2. Linked operational actions and effort

The [attempt schema](../data/schema/verification-attempt-log.schema.json) and [empty CSV header](../data/seed/verification-attempt-log-template.csv) describe event data, not a history that can be reconstructed from inventory method fields. One row is one attempted action, including failures, repeat contacts and reviews. A material-changing action, resident submission, separate evidence assessment and classification review may be separate rows if they are separate activities in the source workflow. Preserve same-day order using linked IDs and the original timestamp/event order in the source mapping ledger; date alone is insufficient.

| Mapping question | Required treatment |
|---|---|
| Initial stock versus new activity | Inventory at the cut-off describes stock. Log a period's actions against linked case IDs; count newly accepted cases once, separately from already accepted baseline cases and later corrections. |
| Outcome mapping | Keep the source outcome in `source_outcome`; map only with a documented reason. An unsupported source acceptance remains preserved in the export while the curated review stays deferred/pending. Do not discard the event or its effort. |
| Review outcomes | Evidence review uses before/after evidence states to distinguish accepted/rejected evidence. An assessment that cannot decide may be `inconclusive` with unchanged state. Classification review separately records `classification_accepted`, `classification_rejected` or `classification_deferred`. |
| Final decision and correction | A reference is not approval. Acceptance needs a pinned, attributed, case/state-matching decision/rule/source bundle. Corrections identify the superseded decision and retain history. See the [workflow contract](workflow-specification.md). |
| Effort | Four effort columns are **staff person-minutes**, including unsuccessful work. Confirm whether the export records elapsed time or summed worker time and how shared travel/review work is allocated. Missing components remain JSON `null`; sum only fully observed components or report an explicit partial total. No missing component becomes zero. |
| Joint/repeated work | Shared effort is counted once with an explicit allocation rule; repeats link to the same case and prior event. Separate both-side outcomes from marginal side outcomes. Do not assume independence. |
| Selection history | Retain source-linked case characteristics, initial state, prior failures, action order, selection reason and existing coarse travel grouping in a restricted companion table. Do not invent absent covariates or drop their missingness. |

The CSV's four state columns contain quoted JSON objects matching the schema. A blank **typed nullable** cell must be mapped explicitly to JSON `null`; it is not the number zero or the literal string `"null"`. Preserve original blank material labels in the received export/mapping ledger. The schema is a draft structural contract, not evidence authentication or an operational importer. The engine requires measured effort for simulation: do not force rows with null effort through it. Retain such rows for coverage review and withhold the affected efficiency comparison.

Complete the [coverage header](../data/seed/attempt-log-coverage-template.csv) for each source/period before estimating rates. It records whether failures, repeats, evidence/classification reviews, corrections, effort and selection histories are captured. Proposed capture values are `complete`, `partial`, `absent`, `unknown`; completeness needs an attributed source audit, not a claim from the research code. Request the actual current workflow, escalation/retry rules and any recording changes during the period. With success-only data, attempt probabilities remain unidentified. With unknown effort, staff-time efficiency remains unavailable for affected comparisons.

## 3. Independent and departmental review

Reviewers should read the [official-source findings](../reports/official-guidance-review.md), [baseline report](../reports/baseline-validation.md), [workflow contract](workflow-specification.md), [second-review response](second-review-response.md) and [review cases](independent-review-checklist.csv). The intake source/rule/decision evidence stays restricted; a reviewer must have authorized access before evaluating real records. The public packet contains no actual decision evidence.

Run `make check` to inspect synthetic contract behavior. Relevant cases in `tests/test_workflow.py` include unsupported Non-Lead acceptance, rejected/deferred review effort, stale/other-case decisions, direct overwrite and valid/invalid corrections. These tests demonstrate the supplied contract only. For R09-R11, inspect dictionary physical pages 2-3 and guidance physical pages 7-12 as indicated by the evidence table; real system-specific approvals and histories are still required. A reviewer should be free to reject the specification or identify missing representation before any importer/model expansion.

For each case record actual reviewer ID/role, date, `review_mode` (`independent_human`, `department_authorized`, `independent_ai`, or `inline_ai_self_review`), source hashes/pages inspected, result, limitations and correction reference. A person is required for `human_verified`. Independent AI review must remain labeled AI. Leave existing `pending` cells unchanged until a real review occurs. This session's source inspection is inline self-review and does not complete any independent or departmental review case.

## 4. First defensible comparison: release conditions

| Gate | Exact evidence still needed |
|---|---|
| Population | Dated system boundary and stable unique line IDs; reviewed crosswalk, row dates and inclusion/exclusion reconciliation. |
| Semantics and rules | Local export mapping; versioned currently applicable category-specific rules, historical lead/extent evidence, approval scope/effective dates and authorized validation. State guidance alone does not confirm local acceptance. |
| Current comparator | Actual sequence, review/queue/escalation/retry practices, who performs each action, and the intended departmental decision. |
| Observations | Linked all-outcome events and independently audited capture coverage for a defined period; submissions, assessments, rejected/deferred reviews and corrections retained. |
| Effort and selection | Person-minute basis, reliable complete effort or explicit unavailable comparisons, action-assignment history, supported initial-state/history overlap and uncertainty assessment. |
| Resources and review | Actual common staff-time/cost constraint, coverage priorities and completed independent/authorized workflow review. |

If these cannot be supplied, stop at the reproducible public-record audit and conditional workflow/intake specification. No local rate, strategy ranking, pilot sample size or preferred allocation follows from this packet. Departmental/resident contact, request submission and field activity remain unauthorized.
