# Douyin Lead Desktop Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a portable Windows desktop application that manages the supplied local APIServer and turns public Douyin comments into a local, exportable lead pipeline.

**Architecture:** Use PySide6 for the desktop shell, SQLite for durable local state, a controlled APIServer subprocess on localhost, and deterministic rule scoring. Package with PyInstaller in one-directory mode so server assets and writable data remain separate.

**Tech Stack:** Python 3.12, PySide6, sqlite3, urllib/httpx-compatible local HTTP, pytest, PyInstaller, Windows DPAPI.

---

### Task 1: Project foundation

**Files:** Create `pyproject.toml`, `app/__init__.py`, `app/paths.py`, `tests/test_paths.py`.

1. Write tests for portable root and writable data paths.
2. Run tests and observe failure.
3. Implement path resolution for source and frozen modes.
4. Run tests and verify pass.

### Task 2: Database and models

**Files:** Create `app/database.py`, `tests/test_database.py`.

1. Test schema creation, unique videos/comments/leads, evidence, rules, tasks and settings.
2. Implement migrations and CRUD helpers.
3. Verify duplicate inserts and task recovery.

### Task 3: Secure settings and APIServer control

**Files:** Create `app/secure_store.py`, `app/server_manager.py`, `tests/test_secure_store.py`, `tests/test_server_manager.py`.

1. Test secret round-trip and redaction.
2. Implement DPAPI with a test fallback only for non-Windows tests.
3. Test command/config preparation without starting the server.
4. Implement start, health check and graceful stop on localhost.

### Task 4: Acquisition engine

**Files:** Create `app/api_client.py`, `app/scoring.py`, `app/collector.py`, tests for each.

1. Test schema-tolerant video/comment parsing.
2. Test intent scoring, spam exclusion, PII masking and deduplication.
3. Implement bounded pagination, request delay, retries, pause/cancel and checkpoints.
4. Verify “销售工牌” fixture reaches deterministic results.

### Task 5: Excel export

**Files:** Create `app/exporter.py`, `tests/test_exporter.py`.

1. Test a valid three-sheet XLSX archive.
2. Implement overview, leads and run-log worksheets with filters and frozen headers.
3. Verify redacted data and Excel readability.

### Task 6: Desktop UI

**Files:** Create `app/main.py`, `app/main_window.py`, `app/pages/*.py`, `app/theme.py`.

1. Add navigation shell and dashboard.
2. Add task creation/progress controls.
3. Add lead, video, rule, history, export and settings pages.
4. Connect background worker signals without blocking the UI.

### Task 7: Packaging and verification

**Files:** Create `build_portable.ps1`, `douyin_lead.spec`, `使用说明.txt`.

1. Copy the supplied APIServer into the bundle staging area without modifying its source ZIP.
2. Build the PyInstaller directory distribution.
3. Launch smoke test, verify database creation and local server diagnostics.
4. Archive the portable directory and report the remaining requirement for a valid per-user order number.
