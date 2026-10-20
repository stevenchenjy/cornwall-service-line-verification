# Independent AI methods review of commit 156ef21

Record: the research lead preserved the following report returned by the read-only child agent `/root/methods_review_156ef21`. The reviewer did not edit project artifacts. The lead's corrections and verification are recorded separately in [the response](../research/methods-review-response-156ef21.md).

---

**Task `MR-156ef21`: request a narrow intake-contract revision.** I found one reproducible medium-priority defect. I found no blocking source-verification findings or critical/high-priority findings. The documentary source conclusions can stand, but the correction-event mismatch should be fixed before describing the attempt schema as ready to retain all outcomes.

| Review field | Value |
|---|---|
| Target commit | `156ef2162c748a4d9f363a678b83c1db5452d448` |
| Review mode | `independent_ai` |
| Actual reviewer identifier | `/root/methods_review_156ef21` |
| Review date | October 20, 2026; checks completed by `2026-10-20T17:15:47Z` |
| Role | Project `methods_reviewer`; separate child agent from the authoring lead |
| Files touched | None |
| Output | This standalone report, returned to the lead |
| Scope of independence | Independent AI artifact review; no human verification, departmental acceptance or authentication of local authority |

**Finding MR-156ef21-F1 — P2: the attempt schema rejects deferred correction events that the workflow retains.**

The new handoff promises retention of attempted actions, failed reviews and correction history in `research/intake-handoff.md:28`, `research/intake-handoff.md:35` and `research/intake-handoff.md:48`. The executable workflow preserves invalid correction effort and defers the correction, as described in `research/workflow-specification.md:35`.

However, `data/schema/verification-attempt-log.schema.json:311` applies its correction condition whenever `action` is `classification_correction`, regardless of outcome. Its consequent requires nonempty strings for both `supersedes_decision_id` and `correction_reason` at lines 321, 326 and 330. Meanwhile, `src/verification_workflow.py:211` populates those fields from the validated record only when acceptance succeeds; a deferred correction can retain `null` values for both.

This is an inherited adjacent schema defect exposed by the new intake handoff, rather than an error in the official-source findings.

Reproduction, run from the repository root:

```bash
.venv/bin/python -B - <<'PY'
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd() / "tests"))
sys.path.insert(0, str(Path.cwd() / "src"))

from test_workflow import WorkflowChecks
from verification_workflow import correct_department_decision

fixture = WorkflowChecks()
fixture.setUp()
try:
    accepted = fixture.accept()
    result = correct_department_decision(
        accepted, effort_minutes=3
    )
    event = result.review_history[-1]
    print(event.action, event.outcome)
    print(event.supersedes_decision_id, event.correction_reason)
    print(result.attempts, result.staff_minutes)
    print(event.validation_error)
finally:
    fixture.doCleanups()
PY
```

Observed result:

```text
classification_correction classification_deferred
None None
2 5
No validated decision bundle supplied; final acceptance remains pending
```

The synthetic fixture’s initial acceptance uses two minutes; the failed correction adds three. The accepted category remains unchanged. Both `null` correction metadata values violate the schema’s nonempty-string conditions. I checked those exact schema predicates directly; I did not run a complete JSON Schema validator, which was unavailable in the inspected Python environments.

**Consequence:** mapping an unsupported correction truthfully into the documented schema fails unless the mapper invents metadata, discards the event or changes its action. Dropping these events would remove correction effort and compromise the promised all-outcome denominator.

**Proportionate correction:** apply the nonempty superseded-ID/reason requirement to accepted corrections. Permit unavailable metadata in rejected/deferred correction attempts while preserving available source values, validation error, unchanged category/evidence and effort. Clarify that incomplete correction metadata keeps acceptance pending. Add a focused regression covering this deferred event and an accepted correction that still lacks required metadata. No broader engine expansion is needed.

Evidence for this finding is the target commit’s schema, engine and synthetic test fixture, independently inspected and executed on the review date. It is a structural contract result, with no inference about real department practice.

**Input and evidence coverage.**

I inspected the target-versus-parent changes across the 32 changed paths, the required project/role instructions, and the relevant adjacent workflow implementation and tests. Primary coverage included:

- `reports/official-guidance-review.md`, `research/official-source-evidence.csv`, `data/manifests/official-guidance-intake.json`, the eight new retrieval receipts and saved originals.
- `research/intake-handoff.md`, all three new baseline/crosswalk/coverage templates, the existing attempt template/schema, and `research/data-dictionary.md`.
- Request, intake, review-checklist, claim/source-register, status/task, decision and workflow documents.
- `scripts/audit_inventory.py`, both generated baseline/preflight report pairs, `src/inventory_audit.py`, `src/verification_workflow.py` and `tests/test_workflow.py`.

Primary evidence pins used in the review:

| Evidence package | Retrieval date/time UTC | SHA256 |
|---|---|---|
| Pinned combined locality snapshot | Manifest finalized `2026-10-20T01:12:38.545211Z`; constituent retrievals retained in its manifest | `4574039b03f11efcf085206f9b3fcb12c32b2ffb9827869829ab2d9f3d73083a` |
| Guidance, main official host; NY-G01–NY-G08 | `2026-10-20T15:30:01.130916Z` | `0666dfbeb6e7944f188e38ded9209530d4707cba720be011405d3a2d28bce951` |
| Attached dictionary; NY-D01–NY-D07 | `2026-10-20T15:30:53.219965Z` | `19123110c1577c86a3951014c782c10e40023dc172f2e6f30efe763c5305868c` |
| Attached overview; NY-O01 | `2026-10-20T15:30:53.682424Z` | `826f1d714fdad2735da96896cb4c936a9e3458bd69d42e8b76bcbb3afb177c84` |
| API metadata; NY-M01 | `2026-10-20T15:30:02.966979Z` | `c4a321119b505b0238db9ec1467c4fe3c13de54c0d04c0d30227e919c0ccf20c` |
| Official directory; NY-S00 | `2026-10-20T15:40:09.710449Z` | `a5da9a1c4b0ed8d5e5abcffefd4f640690c27b4f15320fd6d92d5d4702bae40f` |
| NY3503526 summary; NY-S01–NY-S04 | `2026-10-20T15:40:32.297781Z` | `29d614ace90e81f576c3e8f99194207c5f4a5c855a7b31eafc38c97de4a32bf3` |

The alternate-host guidance receipt also passed hashing and contains identical PDF bytes. Agreement between official hosts does not constitute independent institutional corroboration.

PDF coverage was deliberately bounded: I read saved guidance text for physical pages 1–12, compared fresh extraction from the pinned original for pages 1 and 7–12, and independently viewed existing page renders for pages 8, 11 and 12. I read all dictionary and overview text, compared fresh extraction, and visually inspected dictionary page 2. I did not independently repeat every visual inspection recorded by the author. The guidance index was integrity checked; its complete link inventory and workbook formulas were not re-audited.

**Verification performed and results.**

- `git show`, `git diff` and `git show --check`: target inspected; no whitespace errors. Target equaled local HEAD. The tracked working tree was clean before and after review.
- `PYTHONDONTWRITEBYTECODE=1 make check`: all 24 tests passed; setup/TOML and English checks passed. Tests remain synthetic.
- Read-only SHA256/byte-length checks: all eight new receipts and six archived snapshot receipts matched their saved originals.
- Evidence-table cross-check: 22 distinct evidence IDs; every evidence-row hash and retrieval timestamp matched its referenced receipt.
- Read-only snapshot recomputation using `audit()`, `repeated_record_diagnostics()` and the generator’s aggregate calculations: all 13 recomputed report fields matched `reports/baseline-validation.json`. No reports or duplicate queues were regenerated.
- Template checks: the new baseline, crosswalk and coverage files have one header row and no data rows, with 23, 13 and 19 distinct columns respectively. The existing attempt header has 29 distinct columns and matches schema property order.
- Generated-output inspection: baseline/preflight Markdown files are byte-identical; their JSON files are byte-identical.
- Local-link check: 100 relative Markdown links within changed Markdown paths resolved.
- Privacy inspection: no pinned household-address or coordinate literals were found in changed files; no raw/interim/processed/restricted data files were tracked. Reviewed outputs contain aggregate diagnostics and no individual risk rankings.
- `make preflight` was intentionally not run because it rewrites reports and the restricted duplicate queue. No inventory refetch, Git mutation, push, contact or publication occurred.

**Substantive findings supported by the evidence.**

The public snapshot reproduces **1,110 raw rows and 808 category-Unknown rows**, with **43 repeated address/ZIP groups containing 86 rows** and 43 excess rows under both documented key definitions. Twelve groups differ in overall category; no group has identical material/method/category tuples. These are reproducible raw-record diagnostics, not deduplicated line counts or confirmed revisions. Sources: snapshot hash above, L-C01–L-C03/L-C06, `src/inventory_audit.py:35` and `reports/baseline-validation.md:20`.

The Unknown-category gap buckets reproduce as 575 both-unknown, 176 public-only unknown and 57 customer-only unknown. Full-snapshot material-state counts are 752 public Unknown / 358 public reported-known, and 632 customer Unknown / 478 customer reported-known. Neither side has missing or unmapped labels in this snapshot under the documented normalizer. That absence does not justify zero-filling future missing fields. Source and method: the pinned snapshot, `material_state()` and `audit()`.

The dictionary/metadata mapping supports separating current material, historical public-side lead status, verification method and installation date, while preserving conflicting API descriptions. The PDF headings do not themselves contain API identifiers. Sources: NY-M01, NY-D01–NY-D07, `research/data-dictionary.md:15`. Local export semantics and accepted evidence remain unconfirmed.

The saved summary’s two-cell table rows support **2,553 total** and **1,514 Unknown**, while its certification displays **`10/15/24`**. The directory’s NY3503526 link was independently checked. Sources: NY-S00–NY-S04, `reports/official-guidance-review.md:55`. These are dated reported summary facts; I found no basis for a current population, subtraction, trend or row-membership crosswalk.

The handoff appropriately preserves reported labels, accepted side evidence and accepted category decisions separately; permits sequential work from both-unknown states; distinguishes resident submission from assessment; and requires nullable person-time, shared-effort accounting, joint outcomes and all-outcome coverage review. Sources: `research/intake-handoff.md:28`, `research/intake-handoff.md:36`, workflow implementation and synthetic tests. F1 is the specific exception to the correction-history handoff.

Selection, overlap, current-practice, resource and coverage gates remain explicit. There is no calibrated success-rate estimate, local strategy ranking or household risk inference in this increment.

**Remaining external gates and next handoff.**

Actual system membership, stable unique-line identity, dated baseline/crosswalk, currently applicable authorized rules, historical evidence, validated real decisions, actual current workflow, complete linked attempts, trustworthy effort/selection history, binding resources and coverage priorities remain unavailable. The eight empirical gates stay unconfirmed. This independent AI review does not complete human/departmental review or validate real cases; the acknowledged historical-rule representation limit remains an external acceptance gate, not a newly discovered defect.

The next responsible role is the research lead: preserve this review separately from prior inline self-review, reproduce F1, make the narrow schema/test/documentation correction, run the appropriate checks, and return the revised artifacts for read-only re-review.
