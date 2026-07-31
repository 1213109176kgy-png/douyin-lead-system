from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path


SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS tasks (
 id INTEGER PRIMARY KEY, keyword TEXT NOT NULL, target INTEGER NOT NULL,
 max_videos INTEGER NOT NULL DEFAULT 30, comments_per_video INTEGER NOT NULL DEFAULT 100,
 include_replies INTEGER NOT NULL DEFAULT 0, status TEXT NOT NULL DEFAULT 'pending',
 videos_scanned INTEGER NOT NULL DEFAULT 0, comments_scanned INTEGER NOT NULL DEFAULT 0,
 leads_found INTEGER NOT NULL DEFAULT 0, checkpoint TEXT NOT NULL DEFAULT '{}',
 error TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS videos (
 id INTEGER PRIMARY KEY, aweme_id TEXT NOT NULL UNIQUE, title TEXT NOT NULL DEFAULT '',
 author_uid TEXT NOT NULL DEFAULT '', author_name TEXT NOT NULL DEFAULT '', url TEXT NOT NULL DEFAULT '',
 keyword TEXT NOT NULL DEFAULT '', comment_count INTEGER NOT NULL DEFAULT 0,
 digg_count INTEGER NOT NULL DEFAULT 0, collect_count INTEGER NOT NULL DEFAULT 0,
 leads_found INTEGER NOT NULL DEFAULT 0, scanned_at TEXT NOT NULL DEFAULT '',
 task_id INTEGER, transcript TEXT NOT NULL DEFAULT '', analysis TEXT NOT NULL DEFAULT '',
 rewrite TEXT NOT NULL DEFAULT '', media_url TEXT NOT NULL DEFAULT '',
 archived INTEGER NOT NULL DEFAULT 0, analyzed_at TEXT NOT NULL DEFAULT '',
 material_tags TEXT NOT NULL DEFAULT '', material_note TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS comments (
 id INTEGER PRIMARY KEY, comment_id TEXT NOT NULL UNIQUE, aweme_id TEXT NOT NULL,
 user_key TEXT NOT NULL, user_id TEXT NOT NULL DEFAULT '', nickname TEXT NOT NULL DEFAULT '',
 text TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT '', likes INTEGER NOT NULL DEFAULT 0,
 score INTEGER NOT NULL DEFAULT 0, level TEXT NOT NULL DEFAULT '', matched TEXT NOT NULL DEFAULT '',
 task_id INTEGER
);
CREATE TABLE IF NOT EXISTS leads (
 id INTEGER PRIMARY KEY, user_key TEXT NOT NULL UNIQUE, user_id TEXT NOT NULL DEFAULT '',
 nickname TEXT NOT NULL DEFAULT '', profile_url TEXT NOT NULL DEFAULT '', score INTEGER NOT NULL DEFAULT 0,
 level TEXT NOT NULL DEFAULT '', status TEXT NOT NULL DEFAULT '待跟进', tags TEXT NOT NULL DEFAULT '',
 note TEXT NOT NULL DEFAULT '', keyword TEXT NOT NULL DEFAULT '', evidence_count INTEGER NOT NULL DEFAULT 0,
 first_seen TEXT NOT NULL, last_seen TEXT NOT NULL, task_id INTEGER
);
CREATE TABLE IF NOT EXISTS lead_evidence (
 id INTEGER PRIMARY KEY, lead_id INTEGER NOT NULL, comment_id TEXT NOT NULL UNIQUE,
 aweme_id TEXT NOT NULL, comment_text TEXT NOT NULL, matched TEXT NOT NULL DEFAULT '',
 score INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL DEFAULT '',
 FOREIGN KEY(lead_id) REFERENCES leads(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS rules (
 id INTEGER PRIMARY KEY, category TEXT NOT NULL UNIQUE, weight INTEGER NOT NULL,
 terms TEXT NOT NULL, enabled INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS operation_logs (
 id INTEGER PRIMARY KEY, task_id INTEGER, stage TEXT NOT NULL, target TEXT NOT NULL DEFAULT '',
 status TEXT NOT NULL, found INTEGER NOT NULL DEFAULT 0, message TEXT NOT NULL DEFAULT '',
 created_at TEXT NOT NULL
);
"""


class Database:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.initialize()

    @contextmanager
    def connect(self):
        connection = sqlite3.connect(self.path, timeout=30)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize(self):
        with self.connect() as connection:
            connection.executescript(SCHEMA)
            migrations = {
                "videos": {"task_id": "INTEGER", "transcript": "TEXT NOT NULL DEFAULT ''", "analysis": "TEXT NOT NULL DEFAULT ''", "rewrite": "TEXT NOT NULL DEFAULT ''", "media_url": "TEXT NOT NULL DEFAULT ''", "digg_count": "INTEGER NOT NULL DEFAULT 0", "collect_count": "INTEGER NOT NULL DEFAULT 0", "archived": "INTEGER NOT NULL DEFAULT 0", "analyzed_at": "TEXT NOT NULL DEFAULT ''", "material_tags": "TEXT NOT NULL DEFAULT ''", "material_note": "TEXT NOT NULL DEFAULT ''"},
                "comments": {"task_id": "INTEGER"},
                "leads": {"task_id": "INTEGER"},
            }
            for table_name, columns in migrations.items():
                existing = {row[1] for row in connection.execute(f"PRAGMA table_info({table_name})")}
                for name, definition in columns.items():
                    if name not in existing:
                        connection.execute(f"ALTER TABLE {table_name} ADD COLUMN {name} {definition}")
            connection.execute("UPDATE videos SET task_id=(SELECT id FROM tasks WHERE tasks.keyword=videos.keyword ORDER BY id DESC LIMIT 1) WHERE task_id IS NULL")
            connection.execute("UPDATE comments SET task_id=(SELECT task_id FROM videos WHERE videos.aweme_id=comments.aweme_id) WHERE task_id IS NULL")
            connection.execute("UPDATE leads SET task_id=(SELECT id FROM tasks WHERE tasks.keyword=leads.keyword ORDER BY id DESC LIMIT 1) WHERE task_id IS NULL")
            connection.execute("UPDATE videos SET archived=1,analyzed_at=COALESCE(NULLIF(analyzed_at,''),scanned_at) WHERE analysis<>'' AND archived=0")
            from .scoring import DEFAULT_RULES
            for category, (weight, terms) in DEFAULT_RULES.items():
                connection.execute("INSERT OR IGNORE INTO rules(category,weight,terms,enabled) VALUES(?,?,?,1)", (category, weight, terms))

    def create_task(self, keyword: str, target: int, max_videos: int = 30, comments_per_video: int = 100, include_replies: bool = False) -> int:
        now = datetime.now().isoformat(timespec="seconds")
        with self.connect() as connection:
            cursor = connection.execute(
                "INSERT INTO tasks(keyword,target,max_videos,comments_per_video,include_replies,created_at,updated_at) VALUES(?,?,?,?,?,?,?)",
                (keyword, target, max_videos, comments_per_video, int(include_replies), now, now),
            )
            return int(cursor.lastrowid)

    def update_task(self, task_id: int, **values):
        allowed = {"status", "videos_scanned", "comments_scanned", "leads_found", "checkpoint", "error"}
        values = {k: (json.dumps(v, ensure_ascii=False) if k == "checkpoint" and not isinstance(v, str) else v) for k, v in values.items() if k in allowed}
        values["updated_at"] = datetime.now().isoformat(timespec="seconds")
        fields = ",".join(f"{key}=?" for key in values)
        with self.connect() as connection:
            connection.execute(f"UPDATE tasks SET {fields} WHERE id=?", (*values.values(), task_id))

    def list_tasks(self, limit: int = 200):
        with self.connect() as connection:
            return connection.execute("SELECT * FROM tasks ORDER BY id DESC LIMIT ?", (limit,)).fetchall()

    def get_task(self, task_id: int):
        with self.connect() as connection:
            return connection.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()

    def upsert_video(self, video: dict, keyword: str, task_id: int | None = None):
        with self.connect() as connection:
            connection.execute(
                """INSERT INTO videos(aweme_id,title,author_uid,author_name,url,keyword,scanned_at,task_id,digg_count,collect_count,comment_count)
                VALUES(?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(aweme_id) DO UPDATE SET title=excluded.title,url=excluded.url,keyword=excluded.keyword,task_id=excluded.task_id,digg_count=excluded.digg_count,collect_count=excluded.collect_count,comment_count=excluded.comment_count""",
                (video["aweme_id"], video.get("title", ""), video.get("author_uid", ""), video.get("author_name", ""), video.get("url", ""), keyword, datetime.now().isoformat(timespec="seconds"), task_id, video.get("digg_count", 0), video.get("collect_count", 0), video.get("comment_count", 0)),
            )

    def save_qualified_comment(self, video: dict, comment: dict, scored, keyword: str, task_id: int | None = None) -> bool:
        user_key = comment.get("user_id") or f'{comment.get("nickname", "")}:{comment.get("profile_url", "")}'
        now = datetime.now().isoformat(timespec="seconds")
        comment_id = comment.get("comment_id") or f'{video["aweme_id"]}:{user_key}:{abs(hash(comment["text"]))}'
        with self.connect() as connection:
            existing = connection.execute("SELECT id FROM comments WHERE comment_id=?", (comment_id,)).fetchone()
            if existing:
                return False
            connection.execute(
                "INSERT INTO comments(comment_id,aweme_id,user_key,user_id,nickname,text,created_at,likes,score,level,matched,task_id) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                (comment_id, video["aweme_id"], user_key, comment.get("user_id", ""), comment.get("nickname", ""), comment["text"], comment.get("created_at", ""), comment.get("likes", 0), scored.score, scored.level, "；".join(scored.matched), task_id),
            )
            lead = connection.execute("SELECT * FROM leads WHERE user_key=?", (user_key,)).fetchone()
            if lead:
                connection.execute(
                    "UPDATE leads SET score=MAX(score,?),level=CASE WHEN ?>score THEN ? ELSE level END,evidence_count=evidence_count+1,last_seen=? WHERE id=?",
                    (scored.score, scored.score, scored.level, now, lead["id"]),
                )
                lead_id = lead["id"]
            else:
                cursor = connection.execute(
                    "INSERT INTO leads(user_key,user_id,nickname,profile_url,score,level,keyword,evidence_count,first_seen,last_seen,task_id) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    (user_key, comment.get("user_id", ""), comment.get("nickname", ""), comment.get("profile_url", ""), scored.score, scored.level, keyword, 1, now, now, task_id),
                )
                lead_id = cursor.lastrowid
            connection.execute(
                "INSERT INTO lead_evidence(lead_id,comment_id,aweme_id,comment_text,matched,score,created_at) VALUES(?,?,?,?,?,?,?)",
                (lead_id, comment_id, video["aweme_id"], comment["text"], "；".join(scored.matched), scored.score, comment.get("created_at", "")),
            )
        return True

    def list_leads(self, keyword: str = "", level: str = "", limit: int = 5000, task_id: int | None = None, status: str = ""):
        query, params = "SELECT * FROM leads WHERE 1=1", []
        if keyword:
            query += " AND (keyword LIKE ? OR nickname LIKE ? OR user_id LIKE ?)"
            like = f"%{keyword}%"; params.extend([like, like, like])
        if level:
            query += " AND level=?"; params.append(level)
        if task_id:
            query += " AND EXISTS (SELECT 1 FROM lead_evidence e JOIN comments c ON c.comment_id=e.comment_id WHERE e.lead_id=leads.id AND c.task_id=?)"; params.append(task_id)
        if status:
            query += " AND status=?"; params.append(status)
        query += " ORDER BY score DESC,last_seen DESC LIMIT ?"; params.append(limit)
        with self.connect() as connection:
            return connection.execute(query, params).fetchall()

    def list_videos(self, limit: int = 1000, task_id: int | None = None, keyword: str = "", analyzed: str = ""):
        query, params = """SELECT videos.*,
            (SELECT COUNT(DISTINCT e.lead_id) FROM lead_evidence e WHERE e.aweme_id=videos.aweme_id) AS qualified_count
            FROM videos WHERE 1=1""", []
        if task_id:
            query += " AND task_id=?"; params.append(task_id)
        if keyword:
            query += " AND (title LIKE ? OR author_name LIKE ? OR keyword LIKE ?)"
            like = f"%{keyword}%"; params.extend([like, like, like])
        if analyzed == "yes":
            query += " AND analysis<>''"
        elif analyzed == "no":
            query += " AND analysis=''"
        query += " ORDER BY videos.id DESC LIMIT ?"; params.append(limit)
        with self.connect() as connection:
            return connection.execute(query, params).fetchall()

    def get_video(self, aweme_id: str):
        with self.connect() as connection:
            return connection.execute("SELECT * FROM videos WHERE aweme_id=?", (aweme_id,)).fetchone()

    def update_video_ai(self, aweme_id: str, **values):
        allowed = {"transcript", "analysis", "rewrite", "media_url", "archived", "analyzed_at", "material_tags", "material_note"}
        values = {key: value for key, value in values.items() if key in allowed}
        if not values:
            return
        with self.connect() as connection:
            connection.execute(f"UPDATE videos SET {','.join(f'{key}=?' for key in values)} WHERE aweme_id=?", (*values.values(), aweme_id))

    def list_materials(self, keyword: str = "", limit: int = 1000, task_id: int | None = None, rewritten: str = ""):
        query, params = "SELECT * FROM videos WHERE archived=1 AND analysis<>''", []
        if task_id:
            query += " AND task_id=?"; params.append(task_id)
        if keyword:
            query += " AND (title LIKE ? OR keyword LIKE ? OR material_tags LIKE ?)"
            like = f"%{keyword}%"; params.extend([like, like, like])
        if rewritten == "yes":
            query += " AND rewrite<>''"
        elif rewritten == "no":
            query += " AND rewrite=''"
        query += " ORDER BY analyzed_at DESC,id DESC LIMIT ?"; params.append(limit)
        with self.connect() as connection:
            return connection.execute(query, params).fetchall()

    def list_logs(self, task_id: int | None = None, status: str = "", limit: int = 1000):
        query, params = """SELECT operation_logs.task_id,operation_logs.stage,operation_logs.target,
            operation_logs.status,operation_logs.found,operation_logs.message,operation_logs.created_at,
            tasks.keyword AS task_keyword
            FROM operation_logs LEFT JOIN tasks ON tasks.id=operation_logs.task_id WHERE 1=1""", []
        if task_id:
            query += " AND operation_logs.task_id=?"; params.append(task_id)
        if status:
            query += " AND operation_logs.status=?"; params.append(status)
        query += " ORDER BY operation_logs.id DESC LIMIT ?"; params.append(limit)
        with self.connect() as connection:
            return connection.execute(query, params).fetchall()

    def lead_evidence(self, lead_id: int):
        with self.connect() as connection:
            return connection.execute(
                """SELECT e.*,v.title AS video_title,v.url AS video_url
                FROM lead_evidence e LEFT JOIN videos v ON v.aweme_id=e.aweme_id
                WHERE e.lead_id=? ORDER BY e.id DESC""", (lead_id,)
            ).fetchall()

    def list_rules(self):
        with self.connect() as connection:
            return connection.execute("SELECT * FROM rules ORDER BY id").fetchall()

    def enabled_rules(self):
        with self.connect() as connection:
            rows = connection.execute("SELECT category,weight,terms FROM rules WHERE enabled=1").fetchall()
            return {row["category"]: (row["weight"], row["terms"]) for row in rows}

    def save_rule(self, category: str, weight: int, terms: str, enabled: bool = True, rule_id: int | None = None):
        with self.connect() as connection:
            if rule_id:
                connection.execute("UPDATE rules SET category=?,weight=?,terms=?,enabled=? WHERE id=?", (category, weight, terms, int(enabled), rule_id))
                return rule_id
            cursor = connection.execute("INSERT INTO rules(category,weight,terms,enabled) VALUES(?,?,?,?)", (category, weight, terms, int(enabled)))
            return int(cursor.lastrowid)

    def delete_rule(self, rule_id: int):
        with self.connect() as connection:
            connection.execute("DELETE FROM rules WHERE id=?", (rule_id,))

    def update_lead_status(self, lead_id: int, status: str):
        with self.connect() as connection:
            connection.execute("UPDATE leads SET status=? WHERE id=?", (status, lead_id))

    def count_leads(self, keyword: str = "") -> int:
        with self.connect() as connection:
            if keyword:
                return int(connection.execute("SELECT COUNT(*) FROM leads WHERE keyword=?", (keyword,)).fetchone()[0])
            return int(connection.execute("SELECT COUNT(*) FROM leads").fetchone()[0])

    def dashboard(self):
        with self.connect() as connection:
            return {
                "leads": connection.execute("SELECT COUNT(*) FROM leads").fetchone()[0],
                "high": connection.execute("SELECT COUNT(*) FROM leads WHERE level='高'").fetchone()[0],
                "videos": connection.execute("SELECT COUNT(*) FROM videos").fetchone()[0],
                "tasks": connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0],
            }

    def log(self, task_id: int | None, stage: str, status: str, target: str = "", found: int = 0, message: str = ""):
        with self.connect() as connection:
            connection.execute("INSERT INTO operation_logs(task_id,stage,target,status,found,message,created_at) VALUES(?,?,?,?,?,?,?)", (task_id, stage, target, status, found, message, datetime.now().isoformat(timespec="seconds")))
