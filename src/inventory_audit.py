"""Raw-record diagnostics, never an automatic household or service-line deduplicator."""
from collections import Counter, defaultdict
import re
import unicodedata

KNOWN = {'copper', 'plastic', 'known other', 'lead', 'galvanized', 'galvanized requiring replacement', 'non-lead', 'brass', 'cast iron', 'ductile iron', 'steel', 'asbestos cement'}
UNKNOWN = {'unknown', 'unknown but could be lead', 'unknown but unlikely lead'}

def normalized(value):
    return ' '.join(unicodedata.normalize('NFKC', str(value or '')).split()).casefold()

def material_state(value):
    value = normalized(value)
    if not value:
        return 'missing'
    if value in UNKNOWN:
        return 'unknown'
    return 'reported_known' if value in KNOWN else 'unmapped'

def gap(row):
    public = material_state(row.get('current_public_side_sl'))
    customer = material_state(row.get('customer_sl_material'))
    if 'unmapped' in (public,customer):
        return 'unmapped_material'
    if 'missing' in (public,customer):
        return 'missing_material_field'
    if public == customer == 'unknown':
        return 'both_unknown'
    if public == 'unknown':
        return 'public_unknown'
    if customer == 'unknown':
        return 'customer_unknown'
    return 'both_reported_known'

def address_key(row, normalize=False):
    address, zip_code = str(row.get('street_address') or ''), str(row.get('zip_code') or '')
    if not address.strip() or not zip_code.strip():
        return None
    if normalize:
        address = normalized(address)
        zip_code = normalized(zip_code)
    # Keep apartment/unit tokens, punctuation and ZIP extensions. No fuzzy merge.
    return address, zip_code

def duplicate_summary(rows, normalize=False):
    keys = Counter(key for row in rows if (key := address_key(row, normalize)) is not None)
    repeated = [n for n in keys.values() if n > 1]
    return dict(repeated_key_groups=len(repeated), rows_in_repeated_groups=sum(repeated), excess_rows=sum(n-1 for n in repeated),
                missing_key_rows=sum(address_key(row, normalize) is None for row in rows))

def audit(rows):
    unknown = [r for r in rows if normalized(r.get('sl_category')) == 'unknown']
    gaps = Counter(gap(r) for r in unknown)
    categories = Counter(str(r.get('sl_category') or '<missing>') for r in rows)
    unmapped = {}
    for col in ('current_public_side_sl', 'customer_sl_material'):
        unmapped[col] = dict(Counter(str(r.get(col)) for r in rows if material_state(r.get(col))=='unmapped'))
    return dict(raw_rows=len(rows), raw_categories=dict(categories), unknown_category_rows=len(unknown), unknown_gap_buckets=dict(gaps),
                unknown_rows_needing_public_material=gaps['both_unknown']+gaps['public_unknown'],
                resident_only_completion_raw_row_upper_bound=gaps['customer_unknown'],
                exact_address_zip_duplicates=duplicate_summary(rows), conservative_normalized_duplicates=duplicate_summary(rows,True),
                unmapped_material_labels=unmapped,
                nonunknown_category_rows_with_unknown_or_missing_material=sum(normalized(r.get('sl_category'))!='unknown' and gap(r)!='both_reported_known' for r in rows))

def repeated_record_diagnostics(rows):
    groups = defaultdict(list)
    for row in rows:
        key = address_key(row, True)
        if key is not None:
            groups[key].append(row)
    repeated = [group for group in groups.values() if len(group) > 1]
    fields = ['current_public_side_sl', 'public_sl_material', 'customer_sl_material', 'customer_sl_material_1', 'sl_category']
    return dict(
        repeated_groups=len(repeated),
        identical_payload_groups=sum(all(row == group[0] for row in group) for group in repeated),
        identical_material_method_category_groups=sum(len({tuple(row.get(f) for f in fields) for row in group}) == 1 for group in repeated),
        differing_category_groups=sum(len({row.get('sl_category') for row in group}) > 1 for group in repeated),
        decision='Unresolved candidates; no automatic merge or deletion')

def expected_complete(attempts, eligible_records, accepted_complete_probability):
    if not isinstance(attempts, int) or not isinstance(eligible_records, int) or attempts < 0 or eligible_records < 0:
        raise ValueError('Attempt and record counts must be nonnegative integers')
    if accepted_complete_probability is None or not 0 <= accepted_complete_probability <= 1:
        raise ValueError('Explicit calibrated or scenario complete-line probability required (joint probability for both sides)')
    if attempts > eligible_records:
        raise ValueError('Without an explicit repeat-attempt model, each eligible record can be attempted at most once')
    return attempts * accepted_complete_probability
