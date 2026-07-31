from __future__ import annotations

import threading
from dataclasses import dataclass

from .api_client import LocalApiClient, page_info, parse_comments, parse_videos
from .database import Database
from .scoring import redact_pii, score_comment


@dataclass
class CollectorCallbacks:
    progress: callable = lambda *args: None
    log: callable = lambda *args: None


class Collector:
    def __init__(self, db: Database, client: LocalApiClient, callbacks: CollectorCallbacks | None = None):
        self.db = db; self.client = client; self.callbacks = callbacks or CollectorCallbacks()
        self.pause_event = threading.Event(); self.cancel_event = threading.Event()

    def pause(self): self.pause_event.set()
    def resume(self): self.pause_event.clear()
    def cancel(self): self.cancel_event.set()

    def _wait(self):
        while self.pause_event.is_set() and not self.cancel_event.is_set():
            self.cancel_event.wait(0.25)

    def run(self, task_id: int):
        task = self.db.get_task(task_id)
        keyword, target = task["keyword"], task["target"]
        keywords = [x.strip() for x in keyword.replace("，", ",").split(",") if x.strip()]
        self.db.update_task(task_id, status="running", error="")
        self.db.log(task_id, "start", "ok", keyword)
        try:
            _, found_videos = self.client.search_videos(keyword, task["max_videos"])
            videos = found_videos[:task["max_videos"]]
            total_scanned = int(task["comments_scanned"])
            for v_index, video in enumerate(videos, 1):
                self._wait()
                if self.cancel_event.is_set(): break
                self.db.upsert_video(video, keyword, task_id)
                cursor, scanned = "", 0
                while scanned < task["comments_per_video"]:
                    self._wait()
                    if self.cancel_event.is_set(): break
                    payload = self.client.post("/api/douyin/video_comment", {"aweme_id": video["aweme_id"], "count": min(50, task["comments_per_video"] - scanned), "cursor": cursor})
                    comments = parse_comments(payload)
                    if not comments: break
                    for comment in comments:
                        scanned += 1
                        comment["text"] = redact_pii(comment["text"])
                        result = score_comment(comment["text"], keywords, self.db.enabled_rules())
                        if not result.excluded:
                            self.db.save_qualified_comment(video, comment, result, keyword, task_id)
                    more, new_cursor = page_info(payload)
                    if not more or not new_cursor or new_cursor == cursor: break
                    cursor = new_cursor
                total_scanned += scanned
                leads_found = self.db.count_leads(keyword)
                self.db.update_task(task_id, videos_scanned=v_index, comments_scanned=total_scanned, leads_found=leads_found, checkpoint={"video_index": v_index, "cursor": cursor})
                self.callbacks.progress(v_index, len(videos), leads_found)
                if leads_found >= target: break
            status = "cancelled" if self.cancel_event.is_set() else "completed"
            leads_found = self.db.count_leads(keyword)
            self.db.update_task(task_id, status=status, leads_found=leads_found)
            self.db.log(task_id, "complete", "ok", keyword, leads_found, status)
        except Exception as exc:
            self.db.update_task(task_id, status="failed", error=str(exc))
            self.db.log(task_id, "collect", "error", keyword, message=str(exc))
            raise
