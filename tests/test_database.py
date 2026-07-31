from app.database import Database
from app.scoring import score_comment


def test_database_deduplicates_leads_and_keeps_evidence(tmp_path):
    db = Database(tmp_path / "leads.db")
    task_id = db.create_task("销售工牌", 10)
    assert db.get_task(task_id)["status"] == "pending"
    video = {"aweme_id": "v1", "title": "销售工牌", "url": "u"}
    db.upsert_video(video, "销售工牌")
    score = score_comment("多少钱？我要30个", ["销售工牌"])
    first = {"comment_id": "c1", "text": "多少钱？我要30个", "user_id": "u1", "nickname": "采购", "profile_url": "p"}
    second = {"comment_id": "c2", "text": "怎么联系", "user_id": "u1", "nickname": "采购", "profile_url": "p"}
    assert db.save_qualified_comment(video, first, score, "销售工牌")
    assert db.save_qualified_comment(video, second, score_comment(second["text"], ["销售工牌"]), "销售工牌")
    leads = db.list_leads()
    assert len(leads) == 1
    assert leads[0]["evidence_count"] == 2


def test_rules_crud_and_task_filtered_leads(tmp_path):
    db = Database(tmp_path / "leads.db")
    task_id = db.create_task("智能工牌", 5)
    rule_id = db.save_rule("强意向", 9, "马上买|立即下单")
    assert db.enabled_rules()["强意向"][0] == 9
    db.save_rule("强意向", 8, "马上买", False, rule_id)
    assert "强意向" not in db.enabled_rules()
    video = {"aweme_id": "v-task", "title": "智能工牌"}
    db.upsert_video(video, "智能工牌", task_id)
    scored = score_comment("多少钱，我要一个", ["智能工牌"])
    db.save_qualified_comment(video, {"comment_id": "task-c", "text": "多少钱，我要一个", "user_id": "task-u", "nickname": "客户"}, scored, "智能工牌", task_id)
    assert len(db.list_leads(task_id=task_id)) == 1
    lead = db.list_leads(task_id=task_id)[0]
    db.update_lead_status(lead["id"], "跟进中")
    assert db.list_leads(task_id=task_id)[0]["status"] == "跟进中"
    db.delete_rule(rule_id)


def test_analyzed_video_is_archived_as_material(tmp_path):
    db = Database(tmp_path / "materials.db")
    db.upsert_video({"aweme_id": "material-1", "title": "爆款工牌视频", "digg_count": 100}, "工牌")
    db.update_video_ai("material-1", transcript="口播", analysis="# 拆解", archived=1, analyzed_at="2026-01-01")
    materials = db.list_materials("工牌")
    assert len(materials) == 1
    assert materials[0]["analysis"] == "# 拆解"
    db.update_video_ai("material-1", archived=0)
    assert db.list_materials() == []


def test_library_filters_keep_tasks_and_states_separate(tmp_path):
    db = Database(tmp_path / "filters.db")
    first = db.create_task("AI课程", 5)
    second = db.create_task("销售工牌", 5)
    db.upsert_video({"aweme_id": "ai-1", "title": "AI入门课", "author_name": "老师"}, "AI课程", first)
    db.upsert_video({"aweme_id": "badge-1", "title": "工牌介绍", "author_name": "厂家"}, "销售工牌", second)
    db.update_video_ai("ai-1", transcript="口播", analysis="# 拆解", archived=1, analyzed_at="2026-07-31")
    db.update_video_ai("badge-1", transcript="口播", analysis="# 拆解", rewrite="# 仿写", archived=1, analyzed_at="2026-07-31")
    db.log(first, "collect", "ok", "AI课程")
    db.log(second, "collect", "error", "销售工牌", message="测试错误")

    assert [row["aweme_id"] for row in db.list_videos(task_id=first)] == ["ai-1"]
    assert [row["aweme_id"] for row in db.list_videos(keyword="厂家")] == ["badge-1"]
    assert [row["aweme_id"] for row in db.list_materials(task_id=second, rewritten="yes")] == ["badge-1"]
    assert [row["aweme_id"] for row in db.list_materials(rewritten="no")] == ["ai-1"]
    assert len(db.list_logs(task_id=second, status="error")) == 1
