# Setup preflight — service-line inventory

Generated at 2026-10-20T01:13:42.057554+00:00.

Query: `lower(locality) = 'cornwall-on-hudson'`. Raw rows: **1110**. Category Unknown: **808**.
Counts describe public raw records, not current unique households or service lines.

Source: [NYS inventory API](https://health.data.ny.gov/resource/j63k-4n92.json); [exact query, snapshot SHA256 and retrieval receipts](../data/manifests/inventory-snapshot.json).

| Gap within raw category Unknown | Raw records |
|---|---:|
| both_unknown | 575 |
| customer_unknown | 57 |
| public_unknown | 176 |

Rows needing public-side material evidence: **751**.
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
