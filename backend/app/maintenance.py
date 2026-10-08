"""Export corrected images, back up SQLite, or preview/apply retention cleanup."""
import argparse
from contextlib import closing
import hashlib
import json
import shutil
import sqlite3
from datetime import UTC, datetime, timedelta
from pathlib import Path
from app.core.config import UPLOAD_DIR
from app.db.session import SessionLocal, engine
from app.db.models import PredictionLog, Review


def export_reviews(output: Path):
    output.mkdir(parents=True, exist_ok=True)
    records=[]
    with SessionLocal() as db:
        # Legacy databases may contain multiple reviews; use the latest per prediction.
        seen=set()
        for review in db.query(Review).order_by(Review.reviewed_at.desc()).all():
            if review.prediction_id in seen: continue
            seen.add(review.prediction_id)
            prediction=db.get(PredictionLog,review.prediction_id)
            if prediction is None: continue
            source=Path(prediction.image_path).resolve()
            if not source.is_relative_to(UPLOAD_DIR.resolve()) or not source.is_file(): continue
            if review.correct_label not in {'healthy','leaf_spots','severe_damage'}: continue
            digest=hashlib.sha256(source.read_bytes()).hexdigest()
            target=output/review.correct_label/(digest+source.suffix)
            target.parent.mkdir(exist_ok=True)
            if not target.exists(): shutil.copy2(source,target)
            records.append({'image':str(target.relative_to(output)),'sha256':digest,'label':review.correct_label,'prediction_id':review.prediction_id,'reviewed_at':review.reviewed_at.isoformat()})
    (output/'manifest.json').write_text(json.dumps(records,indent=2))
    print(f'Exported {len(records)} reviewed records. Audit and split before adding them to training.')


def backup_database(output: Path):
    if engine.url.get_backend_name() != 'sqlite':
        raise ValueError('Use your database provider backup tool for non-SQLite deployments')
    if output.exists(): raise ValueError('Choose a new backup filename')
    output.parent.mkdir(parents=True,exist_ok=True)
    with closing(sqlite3.connect(engine.url.database)) as source, closing(sqlite3.connect(output)) as target:
        source.backup(target)
    print(f'Database backed up to {output}. Also back up uploaded_images and the model checkpoint.')


def purge(days: int, apply: bool, include_reviewed: bool):
    cutoff=datetime.now(UTC).replace(tzinfo=None)-timedelta(days=days)
    with SessionLocal() as db:
        query=db.query(PredictionLog).filter(PredictionLog.created_at < cutoff)
        if not include_reviewed:
            query=query.filter(~PredictionLog.prediction_id.in_(db.query(Review.prediction_id)))
        predictions=query.all()
        print(f'{len(predictions)} predictions older than {days} days; '+('applying cleanup' if apply else 'dry run (use --apply to delete)'))
        if not apply: return
        paths=[]
        for prediction in predictions:
            path=Path(prediction.image_path).resolve()
            if path.is_relative_to(UPLOAD_DIR.resolve()): paths.append(path)
            db.query(Review).filter(Review.prediction_id==prediction.prediction_id).delete()
            db.delete(prediction)
        db.commit()
        for path in paths: path.unlink(missing_ok=True)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    export=commands.add_parser('export-reviews'); export.add_argument('output',type=Path)
    backup=commands.add_parser('backup'); backup.add_argument('output',type=Path)
    cleanup=commands.add_parser('purge'); cleanup.add_argument('--days',type=int,default=30); cleanup.add_argument('--apply',action='store_true'); cleanup.add_argument('--include-reviewed',action='store_true')
    args=parser.parse_args()
    if args.command=='export-reviews': export_reviews(args.output)
    elif args.command=='backup': backup_database(args.output)
    elif args.days < 1: parser.error('--days must be positive')
    else: purge(args.days,args.apply,args.include_reviewed)

if __name__=='__main__': main()
