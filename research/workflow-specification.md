# Sequential verification and decision-review contract - revised after second review

This is a narrow executable design contract, not Cornwall operating policy or a calibrated allocation model. Actual departmental rules, baseline and workflow are still missing. See [data-intake-plan.md](data-intake-plan.md) for the trust boundary and [independent-review-checklist.csv](independent-review-checklist.csv) for review cases.

## Separate state and outcome

A case retains stable pseudonymous case/system IDs, baseline date, both reported materials and submitted/accepted/rejected evidence references. A fully evidenced pair remains a process milestone. It never automatically creates an accepted category. Category-specific rules can require evidence on one or both sides; the code does not invent regulatory rules.

## Submission, assessment and classification actions

| Action | Eligibility | Outcome and effort |
|---|---|---|
| Public records or targeted/joint field work | Relevant side evidence unaccepted | Returned evidence, no response, inconclusive, access failure or cancellation; retain effort and state |
| Resident assistance | Customer evidence unaccepted, including both-unknown states | A returned resident submission remains submitted; it cannot directly create accepted evidence |
| Evidence review | Submitted evidence exists | Departmental assessment accepts/rejects the submitted side evidence; record its separate effort |
| Classification review | No accepted final category yet | Explicit acceptance, rejection or deferral; every outcome retains effort/history |
| Classification correction | A final category already exists | Separate validated superseding decision and reason; retain old/new category and side-evidence history |

Records review then resident assistance (or reverse) remains possible from both-unknown states. A review may reject/defer while materials remain unknown. The frozen 57-row resident-only bound does not bound resident participation after other actions. Failed attempts and review work do not count as accepted completions.

## Validated final-decision records

The old `rules_confirmed=True` / arbitrary reference interface has been removed. `classification_review()` and `record_department_decision()` require a pinned local decision bundle before acceptance:

- The structured decision record and referenced source document exist and match their SHA256.
- Attributed validation entries identify a reviewer and review date for the decision and rule source; their real authority must be checked during intake.
- Case ID, system ID, baseline date and evidence-state fingerprint match, preventing cross-case and stale-state reuse.
- The reviewed rule category/system and category-specific material/evidence alternatives match the current case; required side evidence files exist and match hashes.
- An accepted initial decision cannot overwrite an existing accepted category.

Missing, malformed, unvalidated, mismatched or insufficient evidence yields a **deferred classification review**, with effort and validation error preserved. A reference string or method label alone cannot produce success. The validators check structural integrity and consistency; they cannot authenticate a forged source or replace substantive department/state review. All actual rule/decision inputs remain absent.

## Corrections and history

`correct_department_decision()` is a separate path. It requires a new decision ID, the superseded decision ID, a correction reason, matching replacement evidence state and the same pinned/validated source checks. Invalid corrections retain the existing category/evidence and record a deferred correction with effort. Valid corrections retain both decisions and before/after side states, so the case remains one classified line rather than two completions.

The [attempt schema](../data/schema/verification-attempt-log.schema.json) distinguishes evidence_review, classification_review and classification_correction. Optional curated fields link validated records, source outcomes and correction history; an existing department export can be mapped without pretending these fields were originally recorded.

Schema v3 requires a nonempty superseded decision ID and reason only for an accepted correction. A rejected/deferred correction attempt can retain null or omitted metadata when it is genuinely unavailable; preserve available source values, validation error, unchanged category/evidence and staff effort. Missing correction support never becomes acceptance. The executable engine's acceptance/correction requirements are unchanged.

## Source-supported intake qualifications - October 20, 2026

The [official-source review](../reports/official-guidance-review.md) supports separate resident submission/staff assessment and documents why historical upstream lead and segment extent may matter to category review. It does not load a local rule or verify a case. The current engine validates supplied side-material evidence patterns; it is not an implementation of all regulatory conditions and cannot itself establish upstream history. An authorized substantive rule/decision review must cover any required historical facts and current applicability before validation. If the real rule cannot be represented adequately, keep acceptance pending and document the representation gap before expanding the engine.

Use the [intake handoff](intake-handoff.md) for baseline/crosswalk and attempt-coverage headers. Nullable effort is preserved during intake even though the synthetic workflow engine requires finite observed effort for execution. Preserve stock versus new-period classifications, same-day action ordering, failed/repeated work and shared person-time before considering a comparison.

## Modeling gate

A dated stable-ID population, confirmed semantics/acceptance rules, actual current workflow, attempt-level effort/outcomes including failures/reviews/retries, and agreed resource/coverage priorities are all required. Preserve case difficulty, action history and selection reasons before comparing observed rates. Synthetic document/time fixtures demonstrate contract behavior, not Cornwall effectiveness. Maps are optional and no optimizer is being built.
