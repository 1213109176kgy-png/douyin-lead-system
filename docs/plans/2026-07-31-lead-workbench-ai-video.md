# Lead Workbench and AI Video Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Improve lead/video tables, add editable intent rules and task-based export, and provide local Whisper transcription plus configurable OpenAI-compatible analysis and rewriting.

**Architecture:** Extend the existing SQLite database with backward-compatible migrations and repository methods. Keep UI actions in PySide dialogs and run download/transcription/LLM work in background threads. Use `faster-whisper` base INT8 locally, an OpenAI-compatible chat endpoint for DeepSeek, and store secrets through the existing DPAPI settings store.

**Tech Stack:** Python 3.10, PySide6, SQLite, urllib, faster-whisper, bundled FFmpeg, OpenAI-compatible HTTP APIs.

---

### Task 1: Database migrations and repositories

**Files:**
- Modify: `app/database.py`
- Test: `tests/test_database.py`

1. Add migration-safe columns for task ownership, video analysis, transcript, rewrite, and rule state.
2. Add lead evidence queries, task-filtered lead queries, video detail update methods, and rules CRUD.
3. Seed default rules only when absent.
4. Test migration against an existing database and verify task filtering.

### Task 2: Lead pool expandable details

**Files:**
- Modify: `app/main_window.py`

1. Replace full user ID with a shortened display value.
2. Add original-comment preview and operations columns.
3. Open an expandable detail dialog containing full ID and all evidence.
4. Add a public-profile action and verify the target URL.

### Task 3: Video library actions

**Files:**
- Create: `app/video_ai.py`
- Modify: `app/main_window.py`
- Modify: `app/api_client.py`
- Test: `tests/test_video_ai.py`

1. Add shortened title display and a full-detail dialog.
2. Add view-original, analyze, and rewrite operations.
3. Resolve/download the public video to a local temporary path.
4. Run analysis and rewriting in a background thread with progress and cancellation.

### Task 4: Local Whisper transcription

**Files:**
- Modify: `app/video_ai.py`
- Modify: `pyproject.toml`
- Test: `tests/test_video_ai.py`

1. Download/cache `faster-whisper` base in `data/models`.
2. Run CPU INT8 transcription with Chinese language preference.
3. Persist transcript and delete temporary media after processing.
4. Expose clear download/transcription errors without losing prior results.

### Task 5: AI and prompt settings

**Files:**
- Create: `app/ai_client.py`
- Modify: `app/main_window.py`
- Test: `tests/test_ai_client.py`

1. Add OpenAI-compatible base URL, API key, model, timeout, and temperature.
2. Encrypt API key with DPAPI and provide a connection test.
3. Add editable analysis/rewrite prompt templates with documented variables and reset defaults.
4. Add per-rewrite requirements without modifying global prompts.

### Task 6: Intent rule CRUD

**Files:**
- Modify: `app/main_window.py`
- Modify: `app/scoring.py`
- Modify: `app/collector.py`
- Test: `tests/test_database.py`

1. Add create/edit/enable/delete dialogs with confirmation.
2. Prevent permanent loss of defaults by providing restore-default.
3. Load enabled database rules for every new collection task.
4. Verify scoring changes after editing a rule.

### Task 7: Task-based export

**Files:**
- Modify: `app/exporter.py`
- Modify: `app/main_window.py`
- Test: `tests/test_exporter.py`

1. Replace free-text keyword selection with task, level, and status selectors.
2. Show an export preview count.
3. Include original comments, source video, profile URL, matched rules, and task fields.
4. Verify generated XLSX sheets and task filtering.

### Task 8: Packaging and end-to-end verification

**Files:**
- Modify: `build_portable.ps1`
- Modify: `使用说明.txt`

1. Install and package faster-whisper plus FFmpeg support.
2. Run unit tests, offscreen UI smoke, real APIServer search, and staged EXE launch.
3. Verify a clean ZIP contains no settings, database, API key, or Cookie.
4. Publish a versioned portable ZIP and calculate SHA256.
