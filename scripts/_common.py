from pathlib import Path
from datetime import datetime, timezone
import csv
import hashlib
import urllib.request

ROOT = Path(__file__).resolve().parents[1]

def utc_now():
    return datetime.now(timezone.utc).isoformat()

def download(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'CornwallResearch/0.1 (public-source reproducibility)'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read(), response.geturl(), response.headers.get('Content-Type', '')

def save_raw(source_id, url, data, resolved_url, content_type, extension):
    now = datetime.now(timezone.utc)
    stamp = now.strftime('%Y%m%dT%H%M%S%fZ')
    path = ROOT / 'data/raw' / f'{source_id}-{stamp}.{extension}'
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as stream:
        stream.write(data)
    receipt = dict(source_id=source_id, requested_url=url, resolved_url=resolved_url,
                   retrieved_at_utc=now.isoformat(), sha256=hashlib.sha256(data).hexdigest(),
                   bytes=len(data), content_type=content_type, local_path=str(path.relative_to(ROOT)))
    manifest = ROOT / 'data/manifests/retrievals.csv'
    manifest.parent.mkdir(parents=True, exist_ok=True)
    exists = manifest.exists()
    with manifest.open('a', newline='', encoding='utf-8') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(receipt), lineterminator='\n')
        if not exists:
            writer.writeheader()
        writer.writerow(receipt)
    return receipt

def latest_receipts():
    manifest = ROOT / 'data/manifests/retrievals.csv'
    if not manifest.exists():
        return {}
    with manifest.open(newline='', encoding='utf-8') as stream:
        return {row['source_id']: row for row in csv.DictReader(stream)}
