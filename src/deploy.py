"""Upload dist/dashboard/index.html to the website bucket and invalidate CloudFront.

The target is deliberately NOT stored in this (public) repository. Set:
  PFI_S3_BUCKET   bucket name
  PFI_S3_KEY      object key of the page (e.g. <site-prefix>/<path>/index.html)
  PFI_CF_DIST     CloudFront distribution id (optional, for invalidation)
  PFI_CF_PATHS    comma-separated invalidation paths (optional)
Credentials: AWS_Key / AWS_Pass if present, else the default boto3 chain.
"""
import os
import pathlib
import sys
import time

import boto3

ROOT = pathlib.Path(__file__).resolve().parents[1]


def session():
    k, s = os.environ.get("AWS_Key"), os.environ.get("AWS_Pass")
    if k and s:
        return boto3.session.Session(aws_access_key_id=k.strip(), aws_secret_access_key=s.strip(), region_name="eu-north-1")
    return boto3.session.Session(region_name="eu-north-1")


def main():
    bucket, key = os.environ.get("PFI_S3_BUCKET"), os.environ.get("PFI_S3_KEY")
    if not bucket or not key:
        sys.exit("set PFI_S3_BUCKET and PFI_S3_KEY")
    page = ROOT / "dist" / "dashboard" / "index.html"
    sess = session()
    sess.client("s3").put_object(Bucket=bucket, Key=key, Body=page.read_bytes(),
                                 ContentType="text/html; charset=utf-8",
                                 CacheControl="public, max-age=60, must-revalidate")
    print(f"uploaded {page.stat().st_size / 1024:.0f} KB -> s3://{bucket}/{key}")
    dist = os.environ.get("PFI_CF_DIST")
    if dist:
        paths = [p.strip() for p in os.environ.get("PFI_CF_PATHS", "").split(",") if p.strip()]
        if paths:
            r = sess.client("cloudfront").create_invalidation(
                DistributionId=dist,
                InvalidationBatch={"Paths": {"Quantity": len(paths), "Items": paths}, "CallerReference": str(time.time())})
            print("invalidation", r["Invalidation"]["Id"], r["Invalidation"]["Status"])


if __name__ == "__main__":
    main()
