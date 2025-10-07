ROOT := /Users/markadams/Desktop/idsideAI_PyCharm_Mac_20251006_POLISHED_WITH_RC_PATCHED
BACK := $(ROOT)/idsideAI_FIXED
KIT  := /Users/markadams/Downloads/idsideAI_PATCH_MERGE_KIT_251007
PORT ?= 8013

.PHONY: run stop init-db verify apply-patches run-bg status logs

run:
	cd $(BACK) && uvicorn backend.app:app --host 0.0.0.0 --port $(PORT) --reload

stop:
	@echo "[stop] Killing any process on :$(PORT) ..."
	-@PID=$$(lsof -ti tcp:$(PORT)); \
	  if [ -n "$$PID" ]; then kill -9 $$PID && echo "[stop] Killed $$PID"; else echo "[stop] None found"; fi

init-db:
	cd $(KIT) && DATABASE_URL="sqlite:///$(BACK)/app.db" python init_db.py

verify:
	$(KIT)/verify_endpoints.sh http://127.0.0.1:$(PORT)

apply-patches:
	$(KIT)/apply_patches.sh "$(BACK)"

run-bg:
	cd $(BACK) && nohup uvicorn backend.app:app --host 0.0.0.0 --port $(PORT) --reload > $(BACK)/run.log 2>&1 &
	@echo "[run-bg] started; tail logs with: make logs"

status:
	@lsof -i :$(PORT) || true

logs:
	@tail -n 100 -f $(BACK)/run.log

.PHONY: openapi-guard-local
openapi-guard-local:
	python idsideAI_FIXED/scripts/check_openapi.py http://127.0.0.1:8013

.PHONY: route-audit
route-audit:
	python idsideAI_FIXED/scripts/route_prefix_audit.py http://127.0.0.1:$(PORT)
