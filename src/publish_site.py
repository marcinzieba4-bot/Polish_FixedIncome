"""Publish the live dashboard, the daily archive and every point-in-time report in one pass.

Targets come from the environment (never stored in this public repository):
  PFI_S3_BUCKET  bucket; PFI_S3_PREFIX  key prefix of the /polishfi path; PFI_CF_DIST  CloudFront distribution id
Uploads <prefix>/index.html (dist/dashboard), <prefix>/archive/index.html (dist/archive) and
<prefix>/YYYY-MM-DD/index.html for each data/snapshots/*/dist/index.html, then one invalidation of /polishfi*.
Usage: python src/publish_site.py [--only-archive]
"""
import os
import pathlib
import re
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from deploy import ROOT, session  # noqa: E402


def main():
    bucket, prefix, dist = os.environ.get("PFI_S3_BUCKET"), os.environ.get("PFI_S3_PREFIX", "").rstrip("/"), os.environ.get("PFI_CF_DIST")
    if not bucket or not prefix:
        sys.exit("set PFI_S3_BUCKET and PFI_S3_PREFIX")
    files = {f"{prefix}/archive/index.html": ROOT / "dist" / "archive" / "index.html"}
    if "--only-archive" not in sys.argv:
        files[f"{prefix}/index.html"] = ROOT / "dist" / "dashboard" / "index.html"
        for d in sorted((ROOT / "data" / "snapshots").iterdir()):
            if re.fullmatch(r"\d{4}-\d\d-\d\d", d.name) and (d / "dist" / "index.html").exists():
                files[f"{prefix}/{d.name}/index.html"] = d / "dist" / "index.html"
    s3 = session().client("s3")
    for key, path in files.items():
        s3.put_object(Bucket=bucket, Key=key, Body=path.read_bytes(), ContentType="text/html; charset=utf-8",
                      CacheControl="public, max-age=60, must-revalidate")
    print(f"uploaded {len(files)} pages")
    if dist:
        r = session().client("cloudfront").create_invalidation(
            DistributionId=dist, InvalidationBatch={"Paths": {"Quantity": 1, "Items": ["/polishfi*"]}, "CallerReference": str(time.time())})
        print("invalidation", r["Invalidation"]["Id"], r["Invalidation"]["Status"])


if __name__ == "__main__":
    main()
