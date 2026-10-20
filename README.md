# Cornwall service-line verification workflows

**How can department-approved sequences of records review, resident assistance and field inspection produce more accepted classifications under the same staff-time constraint?** The project is at the departmental data-intake and independent workflow-review handoff stage.

Start with the [public snapshot validation](reports/baseline-validation.md), [sequential workflow specification](research/workflow-specification.md), [revised brief](research/brief.md) and [focused departmental request](research/questions-for-water-department.md).

The pinned locality snapshot contains 1,110 raw records, including 808 Unknown: 575 both-side, 176 public-only and 57 customer-only material gaps. It is not a current system-specific unique-line count. All 43 repeated address/ZIP groups differ in material/method/category data; 12 differ in overall category. No rows were merged.

The revised contract allows sequential records/resident work, separate evidence assessment, and explicit accepted/rejected/deferred classification review with effort. Final decisions require pinned validated source records; corrections preserve superseded decisions and evidence history. Reported material labels, accepted evidence and final department decisions are separate. The 57-row frozen-baseline resident-only bound does not limit resident assistance after public-side work. Tests use synthetic cases and times; no local success rate is estimated.

## Reproduce the audit

```sh
uv sync --locked
make check
make fetch
make preflight
```

Fetching creates ignored local originals. Aggregate reports include exact query and snapshot SHA256. See [START_HERE](START_HERE.md), [status](research/STATUS.md), [task board](research/TASKS.md), [attempt-log schema](data/schema/verification-attempt-log.schema.json) and [initial literature check](research/literature-note.md).

**Modeling gate:** a dated system-specific baseline, stable line IDs, confirmed field and acceptance rules, actual current workflow, attempt-level effort/outcomes and coverage priorities. Costs and probabilities remain null. A public map is optional and does not delay methods review.

This public repository contains English documents, code, schemas, receipts and aggregate results. Household addresses, coordinates, notes, row-level inventory and duplicate queues remain local and ignored. Unknown means insufficient information; no individual risk or local optimum is inferred. No department contact, resident outreach or fieldwork has occurred. Existing agent roles are available; further workspace engineering is paused.

## Next-stage handoff

The [unsent request](research/department-request.md), [intake and selection-bias plan](research/data-intake-plan.md), [independent review cases](research/independent-review-checklist.csv) and [second-review response](research/second-review-response.md) are ready. No actual department rules or decision records have been loaded; structural checks do not authenticate authority.

October 20 evidence increment: the [official-source review](reports/official-guidance-review.md) records successful retrieval and AI text/visual inspection of NYSDOH guidance and the public dataset dictionary. It provides documentary support for the material/method mapping while local applicability remains unconfirmed. The [intake handoff](research/intake-handoff.md) adds empty baseline, restricted crosswalk and event-coverage templates, person-time/missingness rules and independent-review instructions. The public snapshot and all empirical modeling gates are unchanged.
