# Sequential verification workflow — draft contract

This is a reviewable design specification, not an implemented Cornwall operating policy or calibrated allocation model. Departmental acceptance rules, permitted action sequences and retry limits require confirmation. The executable [transition contract](../src/verification_workflow.py) uses no probabilities or optimizer.

## State and outcome

For each stable pseudonymous line/case ID, retain the as-of date and source-row mapping locally. Preserve each side's reported material, evidence status (`unreviewed`, `submitted`, `accepted`, `rejected`) and evidence reference. Preserve the reported overall category separately from the final accepted category, acceptance-rule reference, decision reference and decision date.

A populated method or material label does not imply accepted evidence. `fully_evidenced_pair` is a process milestone; it does not automatically produce an accepted overall category. The final outcome is a documented department-accepted category under a confirmed rule. The contract records such a decision; it does not adjudicate regulatory sufficiency. A confirmed rule may accept a category with one side still unknown, so both known materials are not imposed as a universal completion condition.

## Actions and changing eligibility

| Action | Evidence target | Eligibility before a final accepted decision | Typical next state, conditional on reviewed result |
|---|---|---|---|
| Public records | Public side | Public evidence unaccepted, including both-unknown or a named but unreviewed material | Public evidence submitted/accepted/rejected; customer state retained |
| Resident assistance | Customer side | Customer evidence unaccepted, including both-unknown | Customer evidence submitted/accepted/rejected; public state retained |
| Public/customer field check | Specified side | That side's evidence unaccepted | Reviewed evidence for the target; no automatic result for other side |
| Joint field visit | Either/both sides | At least one side has unaccepted evidence | Separate side outcomes; use observed joint transitions, not an assumed product |
| Classification review | Final category | Documented evidence ready under the confirmed category-specific rule | Accept, reject or defer with a recorded rule and decision |

A both-unknown case can follow `public_records → resident_assisted → classification_review`, or the reverse order, or field escalation. After public records succeed, resident assistance remains eligible. The snapshot's 57 customer-only-unknown raw rows are a frozen-baseline resident-only material-gap bound; they do not bound resident participation after other actions. The 575 both-unknown records are potential sequence inputs, not predicted completions.

No response, inaccessible site, inconclusive evidence and cancellation consume recorded effort and leave evidence unresolved. A returned submission can be rejected or await review. Link retries to earlier attempts; do not count each attempt as a new line or delete failed attempts. Retry caps, waits and escalation criteria remain unset until current practice and constraints are documented. Accepted evidence cannot be silently overwritten; reopening requires a reviewed correction path.

## Calibration and comparison gates

1. Department-confirmed boundary, dated baseline and stable unique-line IDs, with a documented public-row crosswalk and repeated-record treatment.
2. Confirmed evidence/acceptance rules, including conflicting evidence, category-specific sufficiency and update acceptance.
3. Actual current workflow by initial state, including nonresponse, failed access, rejected evidence and follow-up. This is the comparator; do not invent it.
4. Linked attempt logs covering preparation, travel, field/contact work, administration/review and repeat effort. Method distributions in a stock inventory are not attempt success rates.
5. A common staff-time constraint, any monetary constraint and department-defined coverage priorities. Track persistent hard cases, geographic/access differences and selection of easy cases.
6. Independent review of this contract and baseline before strategy results. A map is optional.

Candidate sequences and null parameters are in [scenarios.example.json](../config/scenarios.example.json). Estimate transition probabilities by initial state/action/history with uncertainty only after a defensible attempt denominator exists. Preserve dependence of side outcomes for joint visits. If plausible ranges reverse rankings, identify the next useful measurement instead of choosing a winner.

## Current verification

Synthetic tests demonstrate sequential eligibility, rejected/submitted evidence, nonresponse/retry effort and explicit final acceptance. Synthetic times and rules are test fixtures, not empirical observations. No local success rate, best policy, field protocol or independent review is claimed.
