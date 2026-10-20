# Public inventory snapshot validation

Generated at 2026-10-20T02:09:08.185452+00:00.

Query: `lower(locality) = 'cornwall-on-hudson'`. Raw rows: **1110**. Category Unknown: **808**.
Counts describe public raw records, not current unique households or service lines.

Source: [NYS inventory API](https://health.data.ny.gov/resource/j63k-4n92.json); [exact query, snapshot SHA256 and retrieval receipts](../data/manifests/inventory-snapshot.json).

| Gap within raw category Unknown | Raw records |
|---|---:|
| both_unknown | 575 |
| customer_unknown | 57 |
| public_unknown | 176 |

Rows with public-side material information unknown: **751**.
Resident-only completion raw-record upper bound, assuming acceptable evidence and already reported-known public side: **57**.
This is not a predicted field success count or confirmation of adequate public-side verification.

| Duplicate-key definition | Repeated key groups | Rows in groups | Excess rows |
|---|---:|---:|---:|
| Exact address + ZIP | 43 | 86 | 43 |
| NFKC / whitespace / casefold only; units and punctuation retained | 43 | 86 | 43 |

Duplicate groups are review candidates; no rows were removed or merged.
Non-Unknown category rows with unknown/missing/unmapped material on at least one side: 1.
Some metadata public-side descriptions appear misaligned with display names. The provisional mapping uses names and observed value types; departmental semantic confirmation remains pending.

## Remaining work

- Confirm PWS boundary, stable service-line identifiers, row freshness and duplicate policy.
- Check reported-known material against acceptable verification evidence.
- Calibrate contact rates, accepted evidence rates, time/cost and joint completion.
- Review equity and aggregation before maps or resource recommendations.
- No optimal strategy, current unique line total or individual risk estimate is established.

## Repeated records: additional checks

Of 43 repeated key groups, 0 contain identical full payloads and 0 contain identical material/method/category combinations. 12 groups contain different overall category labels.
These differences do not establish historical revisions or separate lines. A stable identifier and departmental matching policy are needed; all rows remain intact.

## Recorded methods: evidence of filing, not success probabilities

| Side / recorded method | Raw records |
|---|---:|
| Public: `<missing>` | 751 |
| Public: `Excavation` | 45 |
| Public: `Field Inspection` | 17 |
| Public: `Records` | 297 |
| Customer: `<missing>` | 632 |
| Customer: `Excavation` | 16 |
| Customer: `Field Inspection` | 234 |
| Customer: `Records` | 228 |

No attempt denominator, nonresponse history, time, evidence-acceptance decision or line-level date is supplied by these counts. A populated method does not independently establish accepted evidence.

## Research readiness

The public snapshot is reproducible. The allocation population is not department-confirmed. All eight readiness gates in the JSON report remain unconfirmed. Modeling is paused pending the [baseline and attempt-log request](../research/questions-for-water-department.md).

The [state-transition specification](../research/workflow-specification.md) permits public-record review and resident assistance sequentially from both-unknown states. Reported-known labels remain eligible for evidence review. The frozen-baseline resident-only bound of 57 does not bound the contribution of resident assistance after public-side work.

The deterministic transition checks use synthetic cases and times solely to test the contract; they are not Cornwall performance estimates. No independent human or departmental review of the specification has occurred.
