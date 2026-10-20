# Research brief — revised direction

**Question:** Which department-approved sequences of records review, resident assistance and field inspection can produce more accepted service-line classifications under the same staff-time constraint, relative to current practice?

**Current phase:** Validate the population and evidence semantics; specify action sequences before modeling. The reproducible locality snapshot is a public raw-record audit, not a current system-specific unique-line allocation baseline.

**Unit and boundary:** The query `lower(locality) = 'cornwall-on-hudson'` yields 1,110 raw records, including 808 category Unknown. System membership, line IDs and individual as-of dates remain unconfirmed. Relevant utility lines in other localities may be absent. Repeated keys remain unresolved and unmerged.

**Outcome contract:** Preserve raw material labels, reviewed evidence for each side and a documented department-accepted overall category separately. Two named materials do not establish acceptance. Some category decisions may legitimately require a different evidence rule; record the department/state rule rather than hard-coding both sides as universally necessary.

**First increment:** [Snapshot validation](../reports/baseline-validation.md), [sequential workflow contract](workflow-specification.md), synthetic transition tests and an [anonymized attempt-log schema](../data/schema/verification-attempt-log.schema.json). Public-record review followed by resident assistance is permitted from both-unknown states. Rates, costs and acceptance policy remain uncalibrated.

**Modeling gate:** A dated system-specific baseline, reviewed acceptance rules, current workflow, attempt-level effort/outcomes (including failures and repeats), common resource budget and coverage priorities. Without these, produce conditional design questions rather than a local optimum.

**Outputs:** Aggregate baseline audit, transition specification, focused request, then a same-resource comparison and sensitivity analysis if inputs arrive. Maps are optional when geography changes travel or coverage decisions; they do not block methods review.

No health-risk prediction, Unknown-as-lead interpretation, automatic household deduplication, resident contact or fieldwork is authorized. Departmental use and originality remain unestablished.
