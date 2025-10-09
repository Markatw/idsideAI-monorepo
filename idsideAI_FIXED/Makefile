# Simple Makefile for backend control

PORT ?= 8013
APP = backend.app:app

stop:
@echo "[stop] Killing any process on :$(PORT) ..."
@lsof -ti :$(PORT) | xargs kill -9 2>/dev/null || true

run:
cd $(PWD) && uvicorn $(APP) --host 0.0.0.0 --port $(PORT) --reload
