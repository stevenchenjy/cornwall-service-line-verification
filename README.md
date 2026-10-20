# Cornwall service-line verification workflows

**How can department-approved sequences of records review, resident assistance and field inspection produce more accepted classifications under the same staff-time constraint?** The first research phase validates the baseline and workflow before allocating resources.

Start with the [public snapshot validation](reports/baseline-validation.md), [sequential workflow specification](research/workflow-specification.md), [revised brief](research/brief.md) and [focused departmental request](research/questions-for-water-department.md).

The pinned locality snapshot contains 1,110 raw records, including 808 Unknown: 575 both-side, 176 public-only and 57 customer-only material gaps. It is not a current system-specific unique-line count. All 43 repeated address/ZIP groups differ in material/method/category data; 12 differ in overall category. No rows were merged.

The new workflow contract allows public-record review followed by resident assistance from both-unknown states. Reported material labels, accepted evidence and final department decisions are separate. The 57-row frozen-baseline resident-only bound does not limit resident assistance after public-side work. Tests use synthetic cases and times; no local success rate is estimated.

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
