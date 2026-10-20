# Independent AI review of the commander evidence package

Lead record: the initial and closure reports below were returned by the separate read-only project reviewer. Their hashes and line references describe their respective 15-file and 17-file inputs before this final recording and the lead's status updates. The lead reproduced both manifests before making those recording edits. The lead's narrow R09 correction and documentary countercase are recorded separately in [the methods response](methods-review.md#independent-check-and-r09-response). The closure report closes the initial finding; neither report supplies human or departmental validation.

## Initial report SL-COMMANDER-MR01

---

**Task `SL-COMMANDER-MR01`: request one narrow documentation revision.** The increment provides a usable request and a defensible evidence-level protocol. One P2 finding remains in the new R09 review criterion: it treats unresolved upstream history as an automatic reason to defer, although the cited archived guidance includes a category-specific presumption for that situation. I found no critical or high-priority issue.

| Review field | Value |
|---|---|
| Base commit | `a6eeaa42dc1ab754a5778dba3d02474b7c929c94` |
| Reviewed revision | Pinned 15-file working-tree documentation increment |
| Reviewer identifier | `/root/methods_review_156ef21` |
| Review mode | `independent_ai` |
| Review completed | `2026-10-20T18:00:27Z` |
| Files touched | None |
| Deliverable | This standalone returned report |
| Authority boundary | AI artifact review; no human verification, departmental acceptance or current local-policy determination |

**Finding SL-COMMANDER-MR01-F1 — P2: R09 should follow the authorized rule’s treatment of historical uncertainty.**

At `research/intake-handoff.md:72`, R09 says:

> Unresolved history or an unrepresentable rule keeps curated acceptance pending.

The cited source, NY-G06, does not support unresolved history as a universal bar to a category decision. The pinned August 2025 v3 guidance, physical page 1 under the GSLRR definition and physical page 7, item 10, describes a presumption of upstream lead when a system cannot demonstrate that the galvanized line was never downstream of lead.

Source details:

- Evidence ID: **NY-G06**, with NY-G01 providing related definitions.
- Original URL: [NYSDOH service-line inventory guidance](https://www.health.ny.gov/environmental/water/drinking/docs/service_line_inventory_guidance_lcrr.pdf).
- Retrieved: `2026-10-20T15:30:01.130916Z`.
- SHA256: `0666dfbeb6e7944f188e38ded9209530d4707cba720be011405d3a2d28bce951`.
- Issue/locator: August 2025 v3; physical pages **1 and 7**.
- Review method: verified the pinned original’s hash, freshly extracted those two pages with `pypdf`, and confirmed that the relevant text matches the saved extraction.
- Uncertainty: this establishes the contents of that archived document. Its current local applicability remains unconfirmed.

A reproducible documentary counterexample is a **hypothetical** case with accepted evidence of a galvanized segment, unresolved upstream history, an authorized applicable rule adopting that documented presumption, and a substantively validated case-matching decision recording its use. The new R09 sentence would still require deferral solely because the history remains unresolved. That contradicts the intended category-specific rule approach in `research/brief.md` and the workflow contract.

The consequence is an unnecessarily strict review criterion that could exclude a legitimately supported category decision and distort the accepted-classification outcome. It does not establish that any actual Cornwall decision should be accepted.

A proportionate replacement is:

> Apply the authorized rule’s documented historical-evidence or presumption treatment, preserving unresolved history distinctly. Keep curated acceptance pending when applicable authority, required evidence, the case-matching decision or adequate representation is missing.

A generic presumption must not itself authenticate a current local decision. The existing rule/source/decision validation requirements should remain.

To reproduce the issue, compare `research/intake-handoff.md:72` with the pinned guidance’s physical page 1 GSLRR definition and page 7, item 10, then apply both criteria to the hypothetical case above. This is a documentary logic check; no engine change or empirical observation is needed.

I checked the adjacent checklist, data plan, source report and workflow wording. I found **no second explicit requirement that history must always be resolved**. Their references to “applicable” or category-required historical evidence are conditional. The existing checklist’s R09 wording could be clarified alongside the route to mention documented presumption treatment, but the definite defect is the new sentence at `research/intake-handoff.md:72`.

**Substantive assessment of the rest of the increment.**

The request is suitable as a technical attachment for a small department. `research/department-request.md:11` accepts existing documents, links, native summaries and statements of unavailability. Detailed exports are conditional at line 20, with smaller alternatives at line 24. It expressly avoids retrospective invention of logs or missing time. Crosswalk and household evidence remain restricted, and transmission requires user approval.

The 12-case route identifies concrete inputs and stop conditions, separates technical inspection from authorized rule confirmation, and leaves actual case validation pending. Its next three actions assign owners and dependencies without claiming contact or receipt. R09 is the exception requiring correction.

The evidence-level protocol at `research/data-intake-plan.md:31` distinguishes full linked records, compatible partial aggregates and absent operations. It preserves failures, repeats, joint outcomes, evolving eligibility, action history and censoring. It treats nullable/shared person-time separately from elapsed time and blocks affected resource comparisons when effort is unavailable. It also retains comparator, overlap, selection, capacity and fairness requirements. Full records do not automatically support causal effects or an optimum.

Review attribution is now accurate. `reports/official-guidance-review.md:3` distinguishes original inline inspection, the later bounded independent AI source/artifact review and the correction re-review. The preserved preexisting diff confirms the blanket no-independent-review statement that was reconciled. No later review is presented as human verification.

**The earlier MR-156ef21-F1 remains closed.** The v3 schema, engine, attempt header and historical review records are unchanged. This new finding concerns R09’s documentation and does not reopen the correction-schema defect.

**Exact input scope and hashes.**

The supplied manifest matches the actual 15 changed paths against the base commit. Its SHA256 is:

`e63725076943368232edda06874025d29e414743a5c8914074f52dde4e170c8f`

Every listed file matched its individual digest at the beginning and end of review. The scope comprises:

- `START_HERE.md`
- Baseline/preflight Markdown and JSON report pairs
- `reports/methods-review.md`
- `reports/official-guidance-review.md`
- `research/STATUS.md`, `research/TASKS.md`, `research/analysis-plan.md`
- `research/claim-register.csv`, `research/decisions.md`
- The request, intake handoff and data-intake plan

Focused pins:

| Input | SHA256 |
|---|---|
| `research/department-request.md` | `cd00ff3ac01ca876d7c9ad0ee8b773c2a6d3e84e30cebbdc610e0c504a056163` |
| `research/intake-handoff.md` | `1a2d45c9df72f28e393a14a8cd62ee4d1cf85d77657d500f2c09bd8e8279fab7` |
| `research/data-intake-plan.md` | `dd946f926cbaff370ad74e75e2338f69905566975e0d3b77612d8aadee16a4aa` |
| `reports/methods-review.md` | `5a85d27ad023f4947a6bc95c2f2e296062c957965abf1bd4dbae8f77f779afc1` |
| `reports/official-guidance-review.md` | `92de8b4e88357c2fd45aea3251105466e43e9d5f7e15883f78789ff5f7188526` |
| Unchanged v3 schema | `65c66367879b9554b112681c57c81edde35ea1b18ad2c6b8d1da2997a48a1637` |
| Unchanged official evidence table | `632a8bbaad402ff9bdc54767a133271c93a87859c00b462fbba4527988bad7b4` |
| Unchanged official manifest | `28893897d5b45679676cefc29c426d0b3c459d4bf125d7952bcace377bcaf9ee` |

**Verification performed.**

All checks below were performed locally by this reviewer during this review:

- `PYTHONDONTWRITEBYTECODE=1 make check`: **27 tests passed**, plus setup/TOML and English checks.
- `git diff --check`: passed.
- Manifest verification: all **15 pinned files** matched; no extra changed path fell outside the manifest.
- Adjacent comparisons against the base: engine, schema, primary evidence table/manifest, attempt header, checklist and historical review/response records are byte-unchanged.
- Official originals: all **eight receipt hashes and byte lengths** matched.
- Snapshot: SHA256 remains `4574039b03f11efcf085206f9b3fcb12c32b2ffb9827869829ab2d9f3d73083a`.
- Baseline JSON: only `generated_at_utc` changed. Both generated report pairs match byte for byte.
- Gates: all **12 human/departmental cases remain pending**; all **eight empirical gates remain unconfirmed**.
- Links: **154 relative Markdown links** resolved; none were broken.
- Privacy: no pinned household-address or coordinate literals were found in the 15 inputs; no private data roots are tracked. Reviewed outputs omit individual risk rankings.

I did not run preflight, install dependencies, refetch inventory, change Git state, contact anyone or publish anything. I did not repeat the earlier PDF visual inspection. New primary-text inspection was limited to the two NY-G06 pages needed for this finding. I did not independently repeat the lead’s 13-case schema matrix in this documentation-only review; the unchanged tests ran successfully, and the earlier independent re-review remains preserved.

**Remaining gates and next handoff.**

The locality snapshot of 1,110 raw rows / 808 Unknown remains separate from the NY3503526 summary of 2,553 total / 1,514 Unknown with displayed certification `10/15/24`. No common population, subtraction, trend or current unique-line count follows.

Actual local rules, dated identity/crosswalk, decision evidence, operational coverage, measured effort, assignment history and departmental constraints remain absent. This review supplies none of them.

The research lead should preserve this report, revise R09 to use the authorized rule’s evidence or presumption treatment, and return the narrow changed wording for read-only closure verification. The staged request and protocol can otherwise stand. User approval of the shared introduction, recipients, attachments and transfer arrangements remains the next external-action gate.

## Closure report SL-COMMANDER-MR01-R1

**Task `SL-COMMANDER-MR01-R1`: the R09 finding is closed at the reviewed pins.** The revised wording allows an authorized rule’s documented presumption treatment without converting unresolved history into observed fact or automatically accepting an archived presumption. No residual or new material finding remains.

| Review field | Value |
|---|---|
| Reviewer identifier | `/root/methods_review_156ef21` |
| Review mode | `independent_ai` |
| Completed | `2026-10-20T18:03:53Z` |
| Base commit | `a6eeaa42dc1ab754a5778dba3d02474b7c929c94` |
| Files touched | None |
| Scope | Narrow read-only documentary closure verification |

**Closure reasoning.**

At `research/intake-handoff.md:72`, R09 now requires the authorized rule’s evidence or presumption treatment, preserves unresolved history distinctly, and keeps acceptance pending when authority, required evidence, a case-matching decision or adequate representation is missing.

The clarification at `research/intake-handoff.md:79` explicitly distinguishes the archived presumption from authentication of a current local decision. `research/independent-review-checklist.csv:10` follows the same rule-dependent approach.

I checked both documentary countercases recorded at `reports/methods-review.md:53`:

- **Applicable-authority countercase:** when a genuinely applicable authorized rule permits the documented presumption and a substantively validated case-matching decision uses it, unresolved history alone no longer forces deferral.
- **Missing-authority/support countercase:** archived guidance alone, or missing authority, required support, valid decision or adequate representation, still leaves acceptance pending.

These are hypothetical logic checks, not evidence of an actual approved local decision. The wording does not automatically accept GSLRR, rewrite Unknown as a known historical material, or expand the engine.

The source clarification is consistent with **NY-G06**, August 2025 v3 guidance, physical page 1’s GSLRR definition and page 7, item 10. That source was retrieved at `2026-10-20T15:30:01.130916Z`, SHA256:

`0666dfbeb6e7944f188e38ded9209530d4707cba720be011405d3a2d28bce951`

My initial commander review independently checked those pages’ extracted text against the pinned original. This closure review did not repeat extraction or visual inspection, and does not establish current local applicability.

**Exact scope and pins.**

All **17 entries** in `work/commander-evidence-stage/r1-input-manifest.sha256` matched the actual files. The manifest SHA256 is:

`81e4e38b27fe852e850e5fa7f904c77b05e19f09f69cfb8c674424a6665d9b22`

Compared with the original reviewed 15-file manifest, only these four inputs changed:

| Changed input | SHA256 |
|---|---|
| `research/intake-handoff.md` | `8c4e3d9794835c1de6bb1f8cd61e1630fa0703bda913ff1b2d04a12efa26d943` |
| `reports/methods-review.md` | `0a3b3487ccc978ab943cf0442cd7aa5dd0fdd44634bbe030f566be8ee5874e49` |
| `research/claim-register.csv` | `fcfee94cf06194f0d6ff910325638616f6107276bd293ca4d94a38bb7edda693` |
| `research/decisions.md` | `598ee8855379f5fa02517e3745dcb6725fa16530b4fa1b098710cf5afbc58b93` |

Two paths were added to the closure scope:

| Additional input | SHA256 |
|---|---|
| `research/independent-review-checklist.csv` | `8778e9b4939e2bde335c4eb00f7b6e4157c6effc7ed1772deb09c47c1a828b81` |
| Preserved initial report, `reports/commander-methods-review.md` | `1c5e2996466c7d181fcaea345302d04950a1603ffdf079b6e5bba10b90a8232b` |

The request, empirical protocol, primary source report and generated report content retain their previously reviewed pins.

**Verification performed.**

- Verified both manifest hashes and all 17 current file digests.
- Parsed the checklist and compared it with the base commit: **only R09’s `expected_behavior` changed**. All 12 statuses remain `pending`; all reviewer/result fields remain blank.
- Inspected the revised R09, clarification, response, countercases, C19 and decision-log entry.
- Searched adjacent handoff, checklist, data-plan, workflow and source/methods-report wording. No active unconditional requirement to resolve all upstream history remains. Historical descriptions of the corrected defect remain appropriately identified.
- Confirmed engine, v3 schema, attempt header, primary evidence table and primary manifest are byte-unchanged from the base.
- Confirmed all eight empirical gates remain unconfirmed and both generated report pairs still match.
- `git diff --check` passed.

I did not rerun the unchanged test suite; the initial commander review’s 27-test result remains applicable to this documentation-only correction. I did not run preflight, install dependencies, fetch data, mutate Git, contact anyone or publish anything.

**Finding status and next handoff.**

- **SL-COMMANDER-MR01-F1 — R09:** closed.
- **MR-156ef21-F1 — correction schema:** remains closed.
- **Residual findings:** none within this narrow scope.

The lead should preserve this closure report separately from the initial finding and update its status references. All 12 human/departmental case checks and eight empirical gates remain open. No actual policy, case decision, operational data, success rate or departmental acceptance follows from this AI artifact review.
