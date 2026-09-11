"""Create disjoint, exact-deduplicated train/validation/test manifests without moving images."""
import hashlib
import json
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ML_DIR = Path(__file__).resolve().parent
REPORTS = ML_DIR / 'reports'

def main():
    labels = json.loads((ML_DIR / 'labels.json').read_text())
    groups = defaultdict(list)
    paths = [p for split in ('train', 'val') for p in (ML_DIR / 'data' / split).rglob('*') if p.is_file() and p.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}]
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest(), path.relative_to(ML_DIR).as_posix()
    with ThreadPoolExecutor(max_workers=8) as pool:
        for sha, path in pool.map(digest, paths):
            groups[sha].append(path)
    conflicts = [sha for sha, names in groups.items() if len({Path(name).parent.name for name in names}) != 1]
    if conflicts:
        raise ValueError(f'{len(conflicts)} identical images have conflicting labels; resolve them first')
    manifest = {'train': [], 'val': [], 'test': []}
    candidates = defaultdict(list)
    overlaps = 0
    for sha, names in sorted(groups.items()):
        train = sorted(n for n in names if n.startswith('data/train/'))
        validation = sorted(n for n in names if n.startswith('data/val/'))
        if train:
            manifest['train'].append(train[0])
            overlaps += bool(validation)
        else:
            candidates[Path(validation[0]).parent.name].append((sha, validation[0]))
    for label in labels:
        entries = candidates[label]
        if len(entries) < 2:
            raise ValueError(f'Not enough held-out images for {label}')
        # Hash ordering gives a repeatable partition, with each duplicate group kept together.
        midpoint = len(entries) // 2
        manifest['val'].extend(path for _, path in entries[:midpoint])
        manifest['test'].extend(path for _, path in entries[midpoint:])
    summary = {'source_images':len(paths), 'unique_images':len(groups), 'cross_split_duplicate_groups':overlaps,
               'counts':{split:{label:sum(Path(p).parent.name == label for p in entries) for label in labels} for split,entries in manifest.items()},
               'limitations':'Exact file hashes only; near duplicates, source-plant grouping and real-phone-photo generalization require a separate audit.'}
    REPORTS.mkdir(exist_ok=True)
    (REPORTS/'splits.json').write_text(json.dumps(manifest,indent=2))
    (REPORTS/'dataset_audit.json').write_text(json.dumps(summary,indent=2))
    print(json.dumps(summary,indent=2))

if __name__ == '__main__':
    main()
