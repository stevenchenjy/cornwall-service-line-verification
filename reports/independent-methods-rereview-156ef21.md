# Independent AI methods re-review MR-156ef21-R1

Lead recording note: the body below preserves the separate read-only agent's returned re-review of the correction to commit `156ef21`. Its hashes and line references describe the 27-file working tree at review completion, before this report was saved and before the lead updated review status and the nonblocking L-C12 attribution note. The lead reproduced the input-manifest hash before making those recording edits. The initial report remains separate and unchanged; the [lead response](../research/methods-review-response-156ef21.md) records the subsequent editorial cleanup and corrective verification. This is independent AI artifact review, not human or departmental acceptance.

---

**Task `MR-156ef21-R1`: F1 is closed in the reviewed working tree.** The revised schema retains failed correction events without weakening the metadata requirements for accepted corrections. I found no new material issue and no blocking findings. One nonblocking attribution cleanup remains in the claim register.

| Review field | Value |
|---|---|
| Base commit | `156ef2162c748a4d9f363a678b83c1db5452d448` |
| Reviewed revision | Uncommitted working-tree correction against that base |
| Reviewer identifier | `/root/methods_review_156ef21` |
| Review mode | `independent_ai` |
| Review completed | `2026-10-20T17:28:50Z` |
| Files touched by reviewer | None |
| Review boundary | Local AI artifact verification; no human or departmental acceptance |

**F1 closure evidence.**

At `data/schema/verification-attempt-log.schema.json:311`, the conditional now requires both `action = classification_correction` and `outcome = classification_accepted` before imposing nonempty `supersedes_decision_id` and `correction_reason`. The accepted-correction requirements remain intact.

I independently compared the original v2 schema, obtained with `git show`, with the working-tree v3 schema using `jsonschema 4.26.0` and `Draft202012Validator`. Test records were mapped from actual synthetic engine review events using `tests/test_attempt_schema.py:28`, with accepted corrections constructed through its fixture at line 53.

| Independently checked case group | Cases | v2 result | v3 result |
|---|---:|---|---|
| Deferred/rejected correction with null metadata | 2 | Invalid | Valid |
| Deferred/rejected correction with partially available metadata | 2 | Invalid | Valid |
| Deferred/rejected correction with both metadata fields omitted | 2 | Invalid | Valid |
| Accepted correction with complete metadata | 1 | Valid | Valid |
| Accepted correction with either field null, empty or omitted | 6 | Invalid | Invalid |
| **Total** | **13** | Expected results reproduced | Expected results reproduced |

The original failure therefore remains reproducible against v2 and is corrected in v3. Failed events retain their outcome, effort and existing accepted category; unsupported correction metadata does not become an accepted replacement decision. These are synthetic structural results, not observations of department practice.

The correction is consistent with `research/intake-handoff.md:35`, `research/intake-handoff.md:42`, `research/workflow-specification.md:39`, the intake plan, data documentation and unsent request. The executable engine and the 29-field CSV header are byte-unchanged from the base commit.

**Verification commands and results.**

- `PYTHONDONTWRITEBYTECODE=1 make check`: **27 tests passed**, including the three new full-schema regressions; setup/TOML and English checks passed.
- `uv sync --locked --check`: succeeded and reported **“Would make no changes.”**
- Independent in-memory v2/v3 validation: both schemas passed `Draft202012Validator.check_schema()`; all **13 countercases** produced their expected results.
- `git diff --check`: passed.
- Read-only byte/hash comparisons: engine, attempt header, independent-review checklist, official-guidance manifest and official-source evidence table match the base commit.
- Baseline JSON comparison against the base: **only `generated_at_utc` changed**. All aggregate values and eight readiness gates are unchanged.
- Baseline/preflight Markdown copies match byte for byte; their JSON copies also match. I inspected the added report narrative and corresponding generator changes.
- Local Markdown link check: **128 relative links resolved; none broken**.
- All **12 human/departmental case statuses remain pending**; all **eight empirical readiness gates remain unconfirmed**.
- Privacy check: no pinned household-address or coordinate literals appeared in the 27 reviewed changed/new files; no raw/interim/processed/restricted data files are tracked. The reviewed outputs contain no individual risk rankings.

I did not run `make preflight`, rewrite reports or queues, install dependencies, fetch inventory, mutate Git, contact anyone or publish anything. The lead’s preflight execution remains its recorded action; my re-review verified the resulting files through read-only inspection and comparisons.

**Dependency and CI alignment.**

`pyproject.toml:11` places the validator in the development dependency group. Runtime research dependencies remain empty. The lockfile and installed validator both identify `jsonschema 4.26.0`.

`.github/workflows/check.yml:13` installs `uv`, runs `uv sync --locked`, then runs `make check`. This includes the validator regressions on the configured fresh-checkout path. **Hosted CI execution has not been observed**, so this review confirms configuration and local execution, not a successful hosted run.

**Exact input scope and hashes.**

I reviewed the 24 modified paths and three untracked artifacts present at the start and end of this re-review:

```text
.github/workflows/check.yml
README.md
START_HERE.md
data/README.md
data/schema/verification-attempt-log.schema.json
pyproject.toml
reports/README.md
reports/baseline-validation.json
reports/baseline-validation.md
reports/methods-review.md
reports/official-guidance-review.md
reports/preflight.json
reports/preflight.md
research/STATUS.md
research/TASKS.md
research/analysis-plan.md
research/claim-register.csv
research/data-intake-plan.md
research/decisions.md
research/department-request.md
research/intake-handoff.md
research/workflow-specification.md
scripts/audit_inventory.py
uv.lock
reports/independent-methods-review-156ef21.md
research/methods-review-response-156ef21.md
tests/test_attempt_schema.py
```

For these 27 paths, I calculated a sorted manifest consisting of one UTF-8 line per file, formatted as `<SHA256><two spaces><repository-relative path>\n`. Its SHA256 is:

`717c7c2fbcab754bab4497791e5a839db12f9c1d2ee896838be710a81f8ed843`

Focused evidence pins:

| Evidence ID | Input | SHA256 |
|---|---|---|
| R1-E01 | Original v2 schema from the base commit | `d7d6e6c329b79f12ac23b8292ffeb7750b5d293cfdd8822411a3c0afa7146cb9` |
| R1-E02 | Working-tree v3 schema | `65c66367879b9554b112681c57c81edde35ea1b18ad2c6b8d1da2997a48a1637` |
| R1-E03 | `tests/test_attempt_schema.py` | `72ab5f9c329b9e954335e87f004ece0a1b6038f088ff87abbd1fa9b32c3f4e81` |
| R1-E04 | `pyproject.toml` | `78a6e51bc374a7a91354a5a3e6b4021c75c203fc1dcfa0a97bc92839f87cb95a` |
| R1-E05 | `uv.lock` | `f896504c83ff4dc629acfc4151b3f04ff0ff607722aa5a36c31862f082339291` |
| R1-E06 | CI workflow | `d1654d8d4f0601a5a7c6b68a783cb6e40c2a5a86efa7ec51e996d0aa9f18362e` |
| R1-E07 | Preserved initial independent report | `46ac5a27d6350042f769787d3cc17fb5b3aa27a50440efbfb077ee9e661997a5` |
| R1-E08 | Lead’s response | `d935899976aab09ea9cabc3e6c84d1e93987150f395be0aa126ee399bd85ebcf` |

The pinned locality snapshot still hashes to:

`4574039b03f11efcf085206f9b3fcb12c32b2ffb9827869829ab2d9f3d73083a`

This re-review did not repeat the primary-source PDF inspection. The source manifest and evidence table are byte-unchanged; their bounded inspection coverage remains recorded in the initial independent report. That report is preserved with a lead attribution wrapper, while the correction response remains separate.

**Residual observation R1-O1 — nonblocking editorial cleanup.**

`research/claim-register.csv:13`, claim L-C12, still says “No populated departmental data or completed independent review,” while L-C15 at line 16 records the completed independent AI review.

Reproduce with:

```bash
rg -n 'L-C12|L-C15' research/claim-register.csv
```

Qualify L-C12 as the state of the original increment, or replace its limitation with wording that distinguishes the completed AI artifact review from pending human/departmental checks. This does not affect F1 closure, numerical results or empirical gates. The preserved historical review should remain unchanged.

**Limits and next handoff.**

This closes the specific schema mismatch at the reviewed hashes. It does not establish department policy, real-case sufficiency, complete operational capture, calibrated effort, success rates, a current unique-line population or an allocation recommendation. Actual policy and operational data remain absent. All 12 human/departmental case checks and eight empirical gates remain open.

The research lead should preserve this re-review, make the small L-C12 attribution cleanup, and update correction/re-review status with a link to this report. Hosted CI and any later delivery should be reported only when observed. No further material correction is requested within this re-review’s scope.
