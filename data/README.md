# Data lifecycle

`seed/` holds explicit source status and initial observations; `schema/` defines data fields; `manifests/` records retrieval receipts.
Raw/interim/processed/restricted directories are local-only and ignored by Git. Do not use `git add -f` for these directories.
Raw snapshots are immutable; a later retrieval makes a new timestamped file. SHA256 is for file integrity, not a de-identified person ID.
Only aggregate statistics without addresses or coordinates belong in `reports/`. A fresh clone must run `make fetch` before preflight.
