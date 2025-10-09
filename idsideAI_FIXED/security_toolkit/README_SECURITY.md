# Security Remediation Toolkit
Generated 2025-09-21T21:28:25.037238Z

## Files
- `passwords.py`: bcrypt helpers (`hash_password`, `verify_password`)
- `apply_security_remediations.py`: safe-mode refactor to replace `hashlib.sha256(...).hexdigest()` with `hash_password(...)` and flag `eval/exec` lines; writes a unified patch in `qa_workspace/qc/`.
- `pre-commit-config.yaml`: enables ruff, mypy, bandit, trufflehog on commit.
- `.github/workflows/secure-ci.yml`: CI gates for linting, typing, SAST, deps, secrets.

## Quickstart
```bash
# 1) Add dependency
pip install passlib[bcrypt]

# 2) Generate a patch (no in-place changes)
python security_toolkit/apply_security_remediations.py

# 3) Review patch and apply
git apply qa_workspace/qc/security_autofix_*.patch

# 4) Swap your auth code to use:
from security_toolkit.passwords import hash_password, verify_password
```

## Notes
- If any sha256 usage is **not** password hashing (e.g., content fingerprints), keep it—this tool only generates a patch for your review.
- Replace all `eval/exec` usages manually with explicit logic; the tool flags them for you.
