import csv
import json
import hashlib
import sys
from collections import Counter
from _common import ROOT, utc_now
sys.path.insert(0, str(ROOT / 'src'))
from inventory_audit import audit, address_key, gap, repeated_record_diagnostics, material_state

def main():
    receipt_path = ROOT / 'data/manifests/inventory-snapshot.json'
    if not receipt_path.exists():
        raise SystemExit('No accepted snapshot. Run make fetch first.')
    receipt = json.loads(receipt_path.read_text())
    data = (ROOT / receipt['combined_path']).read_bytes()
    if hashlib.sha256(data).hexdigest() != receipt['combined_sha256']:
        raise SystemExit('Snapshot hash mismatch; stop and inspect local data.')
    rows = json.loads(data)
    result = audit(rows)
    result.update(generated_at_utc=utc_now(), snapshot_sha256=receipt['combined_sha256'], where=receipt['where'], stage='department_data_intake_preparation',
                  limitation='Counts describe public raw records, not current unique households or service lines.')
    result['repeated_record_diagnostics'] = repeated_record_diagnostics(rows)
    result['recorded_method_counts'] = {
        field: dict(Counter(str(row.get(field) or '<missing>') for row in rows))
        for field in ['public_sl_material', 'customer_sl_material_1']}
    result['known_material_rows_without_recorded_method'] = {
        side: sum(material_state(row.get(material)) == 'reported_known' and not row.get(method) for row in rows)
        for side, material, method in [('public','current_public_side_sl','public_sl_material'),('customer','customer_sl_material','customer_sl_material_1')]}
    result['model_readiness'] = {gate: 'unconfirmed' for gate in [
        'system_membership', 'stable_unique_line_ids', 'row_as_of_dates',
        'field_semantics', 'accepted_classification_rules', 'current_workflow_baseline',
        'attempt_level_calibration', 'resource_and_coverage_priorities']}
    (ROOT / 'reports/preflight.json').write_text(json.dumps(result,indent=2)+'\n', encoding='utf-8')
    lines = ['# Public inventory snapshot validation','',f"Generated at {result['generated_at_utc']}.",'',
             f"Query: `{receipt['where']}`. Raw rows: **{result['raw_rows']}**. Category Unknown: **{result['unknown_category_rows']}**.",
                 'Counts describe public raw records, not current unique households or service lines.','',
                 'Source: [NYS inventory API](https://health.data.ny.gov/resource/j63k-4n92.json); [exact query, snapshot SHA256 and retrieval receipts](../data/manifests/inventory-snapshot.json).', '',
             '| Gap within raw category Unknown | Raw records |','|---|---:|']
    for k,v in sorted(result['unknown_gap_buckets'].items()):
        lines.append(f'| {k} | {v} |')
    lines += ['',f"Rows with public-side material information unknown: **{result['unknown_rows_needing_public_material']}**.",
              f"Resident-only completion raw-record upper bound, assuming acceptable evidence and already reported-known public side: **{result['resident_only_completion_raw_row_upper_bound']}**.",
              'This is not a predicted field success count or confirmation of adequate public-side verification.','',
              '| Duplicate-key definition | Repeated key groups | Rows in groups | Excess rows |','|---|---:|---:|---:|']
    for label,key in [('Exact address + ZIP','exact_address_zip_duplicates'),('NFKC / whitespace / casefold only; units and punctuation retained','conservative_normalized_duplicates')]:
        d=result[key]
        lines.append(f"| {label} | {d['repeated_key_groups']} | {d['rows_in_repeated_groups']} | {d['excess_rows']} |")
    lines += ['', 'Duplicate groups are review candidates; no rows were removed or merged.',
              f"Non-Unknown category rows with unknown/missing/unmapped material on at least one side: {result['nonunknown_category_rows_with_unknown_or_missing_material']}.",
              'Some metadata public-side descriptions remain misaligned with display names. The [official dictionary and guidance comparison](official-guidance-review.md) now provides documentary support for the material/method interpretation; local export semantics and acceptance confirmation remain pending.','',
              '## Remaining work','',
              '- Confirm PWS boundary, stable service-line identifiers, row freshness and duplicate policy.',
              '- Check reported-known material against acceptable verification evidence.',
              '- Calibrate contact rates, accepted evidence rates, time/cost and joint completion.',
              '- Review equity and aggregation before maps or resource recommendations.',
              '- No optimal strategy, current unique line total or individual risk estimate is established.']
    d=result['repeated_record_diagnostics']
    lines += ['', '## Repeated records: additional checks', '',
              f"Of {d['repeated_groups']} repeated key groups, {d['identical_payload_groups']} contain identical full payloads and {d['identical_material_method_category_groups']} contain identical material/method/category combinations. {d['differing_category_groups']} groups contain different overall category labels.",
              'These differences do not establish historical revisions or separate lines. Conservative keys can also miss the same address spelled or abbreviated differently. A stable line identifier and departmental crosswalk are needed; all rows remain intact.', '',
              '## Recorded methods: evidence of filing, not success probabilities', '',
              '| Side / recorded method | Raw records |','|---|---:|']
    for field,label in [('public_sl_material','Public'),('customer_sl_material_1','Customer')]:
        for method,n in sorted(result['recorded_method_counts'][field].items()):
            lines.append(f'| {label}: `{method}` | {n} |')
    lines += ['', 'No attempt denominator, nonresponse history, time, evidence-acceptance decision or line-level date is supplied by these counts. A populated method does not independently establish accepted evidence.', '',
              '## Research readiness', '',
              'The public snapshot is reproducible. The allocation population is not department-confirmed. All eight readiness gates in the JSON report remain unconfirmed. Modeling is paused pending the [baseline and attempt-log request](../research/questions-for-water-department.md).', '',
              'The [state-transition specification](../research/workflow-specification.md) permits public-record review and resident assistance sequentially from both-unknown states. Reported-known labels remain eligible for evidence review. The frozen-baseline resident-only bound of 57 does not bound the contribution of resident assistance after public-side work.', '',
              'The deterministic transition checks use synthetic cases, documents and times; they are not Cornwall performance estimates. Final acceptance requires pinned decision/rule/source evidence, attributed validation and matching case/state. Missing or invalid acceptance evidence produces a deferred review with effort retained. Rejected/deferred reviews and separate correction history are represented. No independent human or departmental review of the specification has occurred.', '',
              'The [independent AI methods report](independent-methods-review-156ef21.md) records bounded source/contract checks and one correction-event intake finding. The [response](../research/methods-review-response-156ef21.md) documents schema v3 and its synthetic validator regressions. This artifact review does not confirm real policy, decisions or calibration.', '',
              'Next-stage handoff: [baseline/crosswalk, log-coverage and review instructions](../research/intake-handoff.md), [departmental request draft](../research/department-request.md), [data-intake and selection-bias plan](../research/data-intake-plan.md), and [independent review cases](../research/independent-review-checklist.csv).' ]
    (ROOT / 'reports/preflight.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    (ROOT / 'reports/baseline-validation.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    (ROOT / 'reports/baseline-validation.json').write_text(json.dumps(result,indent=2)+'\n', encoding='utf-8')
    counts = Counter(address_key(r,True) for r in rows if address_key(r,True) is not None)
    with (ROOT / 'data/restricted/duplicate-review.csv').open('w',newline='',encoding='utf-8') as stream:
        fields=['snapshot_sha256','snapshot_row_1based','street_address','zip_code','sl_category','gap','review_status']
        writer=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n'); writer.writeheader()
        for i,row in enumerate(rows,1):
            if counts.get(address_key(row,True),0)>1:
                writer.writerow(dict(snapshot_sha256=receipt['combined_sha256'],snapshot_row_1based=i,
                                     street_address=row.get('street_address',''),zip_code=row.get('zip_code',''),sl_category=row.get('sl_category',''),gap=gap(row),review_status='unresolved_do_not_merge'))
    print(f"Created aggregate preflight: {result['raw_rows']} raw rows / {result['unknown_category_rows']} Unknown. Duplicate review stays local-only.")

if __name__ == '__main__':
    main()
