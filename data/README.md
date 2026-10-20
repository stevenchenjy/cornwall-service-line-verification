# Data lifecycle

`schema/` contains the saved public field definitions and draft anonymized attempt-log contract. `seed/verification-attempt-log-template.csv` is an empty header template; nested state fields should use JSON cells if this CSV format is chosen. It contains no real cases. `manifests/` records immutable retrievals and the pinned inventory snapshot.

Raw/interim/processed/restricted directories are local-only and ignored. Never force-add them. A later retrieval creates a new timestamped file. SHA256 proves file integrity, not a de-identified person ID or a unique service line.

A fresh clone needs `make fetch` before `make preflight`; the public snapshot audit requires the ignored combined response bytes. Method distributions and repeated-key diagnostics are aggregate filing descriptions, not acceptance or success rates. Keep private row crosswalks and duplicate review in restricted storage.

The requested baseline uses stable pseudonymous line IDs and as-of dates. The attempt log links successes, failures and repeats, retains all staff effort and separates material labels, evidence acceptance and final category decisions. Neither export format nor acceptance policy has been confirmed by the department.
