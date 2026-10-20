# Early methods self-review — October 19, 2026

Reviewer: the same AI session that produced the audit and transition contract. This is not independent human or independent-agent review. Inputs inspected: pinned combined snapshot hash, saved before/after metadata and receipts, aggregate diagnostics, selected source literature/code, workflow specification and synthetic tests. Household-level review against departmental records has not occurred.

| Check | Result | Remaining gate |
|---|---|---|
| Public rows versus allocation population | Raw count and exact locality filter retained | Dated system-specific stable line IDs and membership missing |
| Repeated keys | All 43 groups differ in material/method/category tuple; 12 differ in category; no auto merge | Department must establish identities/history and treatment |
| Field mapping | Display names and observed value types support provisional mapping; conflicting descriptions documented | Departmental semantic confirmation pending |
| Material, method, accepted evidence and category | Separated; method counts are descriptive filing counts | Current acceptance rules and evidence review missing |
| Sequential strategies | Synthetic tests cover records then resident assistance from both-unknown, submitted/rejected evidence and explicit final decision | No operational policy or transition rate estimated |
| Failed/repeated work and administration | Nonresponse consumes effort; repeat attempts remain linked by request schema; final decision review adds effort | Actual workflow, retry limits and measured effort missing |
| Eligibility and final outcome | Named but unaccepted labels remain eligible; both accepted sides do not auto-accept a category; external rule may resolve a category with one side unknown | Confirm category-specific rules; engine records rather than adjudicates external decisions |
| Modeling readiness | Eight unconfirmed gates are explicit and scenario inputs null | No strategy ranking until baseline, acceptance, comparator, calibration and priorities pass |

The code's earlier simple expected-completion helper is retained as a legacy single-action calculation, not used to rank sequential strategies. It requires an explicit probability and cannot supply local calibration. No optimizer has been implemented. The map is optional and does not block review.

Independent review should first challenge identity/mapping and the transition/outcome contract. A department-confirmed baseline and attempt log remain prerequisites for a local recommendation.

## Second-review correction - October 20, 2026

The external ChatGPT review found unsupported default-case acceptance, accepted-category overwrite and missing rejected/deferred review events. This session reproduced all three, replaced the boolean/reference interface with pinned validated documentary records, added case/state/category-evidence checks, separated submission/assessment, retained rejected/deferred effort and added an auditable correction path. Synthetic document tests cover valid and invalid countercases. This is not independent human review or authentication of any actual authority; actual rules and department records remain absent.

## Source/intake follow-up - October 20, 2026

The [official-source review](official-guidance-review.md) now supplies dictionary/guidance support for the material/method mapping, while the API's conflicting descriptions remain preserved. Relevant source pages were read and visually inspected inline by the AI session, with exact page coverage/hashes recorded; this is not an independent or human review. Upstream history, segment extent and current applicability must be checked before validating a real rule. The [intake handoff](../research/intake-handoff.md) adds empty baseline/crosswalk/coverage headers, effort/selection rules and review instructions. All 12 independent/departmental cases remain pending and all eight empirical readiness gates remain unconfirmed.
