ROOT := /Users/markadams/Desktop/idsideAI_PyCharm_Mac_20251006_POLISHED_WITH_RC_PATCHED
BACK := $(ROOT)/idsideAI_FIXED
KIT  := /Users/markadams/Downloads/idsideAI_PATCH_MERGE_KIT_251007

run:
cd $(BACK) && uvicorn backend.app:app --host 0.0.0.0 --port 8013 --reload

stop:
pkill -f "uvicorn .*:8013" || true

init-db:
cd $(KIT) && DATABASE_URL="sqlite:///$(BACK)/app.db" python init_db.py

verify:
$(KIT)/verify_endpoints.sh

apply-patches:
$(KIT)/apply_patches.sh "$(BACK)"
