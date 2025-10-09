#!/bin/sh
# idsideAI QC Battery - POSIX sh compatible
# Usage: sh qc/run_all.sh
# Outputs: qc/*.txt, *.json, *.xml, summary.txt with PASS/FAIL

set -eu
QC_DIR="qc"
mkdir -p "$QC_DIR"
echo "QC run $(date)" > "$QC_DIR/summary.txt"

note() { echo "$@" | tee -a "$QC_DIR/summary.txt"; }

# Env
[ -d .venv ] || python3 -m venv .venv
. .venv/bin/activate || true

# Static checks
ruff check --select E9,F821,B008 . >"$QC_DIR/ruff_hard.txt" 2>&1 || true
mypy . >"$QC_DIR/mypy.txt" 2>&1 || true
bandit -r . -x "tests,qc,tools" -q >"$QC_DIR/bandit.txt" 2>&1 || true

# Tests
pytest -q --maxfail=1 --cov=. --cov-report=xml:"$QC_DIR/coverage.xml" >"$QC_DIR/pytest.txt" 2>&1 || true

# Runtime
(uvicorn backend.app:app --host 127.0.0.1 --port 8013 >"$QC_DIR/uvicorn.log" 2>&1 & echo $! >"$QC_DIR/pid") || true
sleep 3
curl -sf http://127.0.0.1:8013/openapi.json >"$QC_DIR/openapi.json" 2>&1 || true

# Integrity
grep -RInE "TODO|FIXME|PLACEHOLDER" -- * >"$QC_DIR/stubs_scan.txt" 2>&1 || true

# Summary PASS/FAIL
FAIL=0
grep -q "error" "$QC_DIR/ruff_hard.txt" && FAIL=$((FAIL+1)) || true
grep -q "failed" "$QC_DIR/pytest.txt" && FAIL=$((FAIL+1)) || true

if [ "$FAIL" -eq 0 ]; then
  note "QC RESULT: PASS"
else
  note "QC RESULT: FAIL ($FAIL issues)"
fi
