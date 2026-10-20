"""Public locality snapshot. Preserves exact page responses locally and detects obvious concurrent updates."""
import json
import hashlib
import urllib.parse
from _common import ROOT, utc_now, download, save_raw

API = 'https://health.data.ny.gov/resource/j63k-4n92.json'
META = 'https://health.data.ny.gov/api/views/j63k-4n92.json'
WHERE = "lower(locality) = 'cornwall-on-hudson'"

def fetch_json(source_id, url):
    data, resolved, content_type = download(url)
    decoded = json.loads(data)
    receipt = save_raw(source_id, url, data, resolved, content_type, 'json')
    return decoded, receipt

def count():
    query = urllib.parse.urlencode({'$select':'count(*) as n', '$where':WHERE})
    result, receipt = fetch_json('inventory-count', API+'?'+query)
    return int(result[0]['n']), receipt

def main():
    metadata, meta_receipt = fetch_json('inventory-metadata-before', META)
    total_before, count_before = count()
    rows = []
    pages = []
    for offset in range(0, total_before, 1000):
        params = {'$where':WHERE, '$order':':id', '$limit':1000, '$offset':offset}
        page, receipt = fetch_json(f'inventory-page-{offset}', API+'?'+urllib.parse.urlencode(params))
        if not isinstance(page, list):
            raise ValueError('Expected an array of records')
        rows.extend(page)
        pages.append(receipt)
    total_after, count_after = count()
    meta_after, meta_after_receipt = fetch_json('inventory-metadata-after', META)
    if not total_before == total_after == len(rows):
        raise SystemExit('Row count changed during retrieval; raw responses retained, snapshot not accepted. Retry make fetch.')
    if metadata.get('rowsUpdatedAt') != meta_after.get('rowsUpdatedAt'):
        raise SystemExit('Dataset updated during retrieval; raw responses retained, snapshot not accepted. Retry make fetch.')
    needed = {'locality','street_address','zip_code','current_public_side_sl','customer_sl_material','public_sl_material','customer_sl_material_1','sl_category'}
    columns = {c['fieldName'] for c in metadata['columns']}
    if not needed <= columns:
        raise SystemExit('Required dataset fields are missing: '+str(needed-columns))
    combined = json.dumps(rows, ensure_ascii=False, indent=2).encode()
    digest = hashlib.sha256(combined).hexdigest()
    path = ROOT / 'data/interim' / f'inventory-locality-{digest[:16]}.json'
    if path.exists():
        if path.read_bytes() != combined:
            raise ValueError('Snapshot hash collision')
    else:
        with path.open('xb') as stream:
            stream.write(combined)
    receipt = dict(dataset='j63k-4n92', generated_at_utc=utc_now(), where=WHERE, order=':id',
                   raw_rows=len(rows), count_before=total_before, count_after=total_after,
                   dataset_rows_updated_at=metadata.get('rowsUpdatedAt'),
                   combined_path=str(path.relative_to(ROOT)), combined_sha256=digest,
                   metadata_before=meta_receipt, metadata_after=meta_after_receipt,
                   count_before_receipt=count_before, count_after_receipt=count_after,
                   page_receipts=pages, warning='Locality does not establish PWS membership; dataset timestamp is not row freshness.')
    fields = [{k:c.get(k) for k in ('name','fieldName','dataTypeName','description')} for c in metadata['columns']]
    schema_path = ROOT / 'data/schema/inventory-fields.json'
    schema_path.parent.mkdir(parents=True, exist_ok=True)
    schema_path.write_text(json.dumps(fields,indent=2,ensure_ascii=False)+'\n', encoding='utf-8')
    (ROOT / 'data/manifests/inventory-snapshot.json').write_text(json.dumps(receipt,indent=2)+'\n', encoding='utf-8')
    print(f'Accepted locality snapshot: {len(rows)} raw rows; exact response pages retained locally; SHA256 {digest}')

if __name__ == '__main__':
    main()
