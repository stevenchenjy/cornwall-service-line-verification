# Data lifecycle

`schema/` contains the saved public field definitions and draft anonymized attempt-log contract. `seed/verification-attempt-log-template.csv` is an empty header template; nested state fields should use JSON cells if this CSV format is chosen. It contains no real cases. `manifests/` records immutable retrievals and the pinned inventory snapshot.

Raw/interim/processed/restricted directories are local-only and ignored. Never force-add them. A later retrieval creates a new timestamped file. SHA256 proves file integrity, not a de-identified person ID or a unique service line.

A fresh clone needs `make fetch` before `make preflight`; the public snapshot audit requires the ignored combined response bytes. Method distributions and repeated-key diagnostics are aggregate filing descriptions, not acceptance or success rates. Keep private row crosswalks and duplicate review in restricted storage.

The requested baseline uses stable pseudonymous line IDs and as-of dates. The attempt log links successes, failures and repeats, retains all staff effort and separates material labels, evidence acceptance and final category decisions. Neither export format nor acceptance policy has been confirmed by the department.

The draft attempt schema is v3. Accepted corrections require nonempty superseded-ID/reason fields; rejected/deferred correction attempts permit genuinely unavailable metadata to remain null or omitted while retaining effort and source/error information. The 29-column CSV header is unchanged. `make check` includes JSON Schema validation of synthetic correction events; this is not an operational importer or authentication of real decisions.

The empty [baseline](seed/service-line-baseline-template.csv), [identity crosswalk](seed/inventory-crosswalk-template.csv) and [operational coverage](seed/attempt-log-coverage-template.csv) headers are documented in the [intake handoff](../research/intake-handoff.md). They contain no rows; filled exports/crosswalks and validation evidence belong in `restricted/`. Preserve historical public-side lead, source categories versus curated acceptance, same-day event order and capture limitations. Nullable effort is intake data, not executable calibrated input.

The [official-guidance manifest](manifests/official-guidance-intake.json) records the successful main/alternate-host PDF retrievals, current metadata and its dictionary/overview attachments. Original PDFs, extracted text and rendered pages remain ignored. `schema/inventory-fields.json` preserves the earlier public metadata including its conflicting descriptions; the [authored interpretation](../research/data-dictionary.md) records documentary support separately.
