#!/usr/bin/env bash
# Build lambda_function/dist/harvester.zip for the Lambda python3.14 runtime.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"
STAGE="$(mktemp -d)"
cleanup() {
    rm -rf "$STAGE"
}
trap cleanup EXIT

"$PYTHON" -m pip install -r "$ROOT/requirements.txt" -t "$STAGE"
cp "$ROOT"/lambda_function/*.py "$STAGE"/
mkdir -p "$STAGE/nltk_data"
cp -a "$ROOT/lambda_function/nltk_data/." "$STAGE/nltk_data/"
find "$STAGE" -type d -name '__pycache__' -prune -exec rm -rf {} +

mkdir -p "$ROOT/lambda_function/dist"
OUT="$ROOT/lambda_function/dist/harvester.zip"
rm -f "$OUT"
(
    cd "$STAGE"
    "$PYTHON" -m zipfile -c "$OUT" .
)
echo "Wrote $OUT"
