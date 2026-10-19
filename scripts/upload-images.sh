#!/usr/bin/env sh
# Upload rendered page images to a Cloudflare R2 bucket with rclone.
#
# One-off setup (https://rclone.org/s3/#cloudflare-r2):
#   rclone config create r2 s3 provider=Cloudflare access_key_id=... secret_access_key=... \
#       endpoint=https://<account id>.r2.cloudflarestorage.com acl=private
# Then make the bucket public (R2 dashboard, "Public access") and set IMAGES_BASE in the
# GitHub repository variables to its public URL, for example https://pub-xxxx.r2.dev.
#
# Usage: scripts/upload-images.sh [bucket]      (default bucket: ncert-pages)
set -eu
cd "$(dirname "$0")/.."
bucket="${1:-ncert-pages}"
uv run ncert-diff render-pages
# Only new or changed files are transferred. Images are immutable per edition, so cache for a year.
rclone copy site/images "r2:${bucket}" --checksum --transfers 16 \
  --header-upload "Cache-Control: public, max-age=31536000, immutable" --progress
