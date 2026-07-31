from app.paths import resolve_paths
from app.douyin_login import cookie_header, has_login_cookie
from app.server_manager import ServerManager
from app.scoring import redact_pii, score_comment


def test_portable_paths(tmp_path):
    paths = resolve_paths(tmp_path).ensure()
    assert paths.database == tmp_path / "data" / "leads.db"
    assert paths.exports.is_dir()


def test_sales_badge_scoring_and_redaction():
    result = score_comment("销售工牌多少钱一个？我们需要30个", ["销售工牌"])
    assert result.level == "高"
    assert result.score >= 7
    assert "[手机号已隐藏]" in redact_pii("联系13800138000")


def test_spam_is_excluded():
    assert score_comment("兼职刷单加微信 abc123456", ["销售工牌"]).excluded


def test_douyin_login_cookie_detection_and_header():
    cookies = {"passport_auth_status": "true", "sessionid_ss": "abc", "other": "x"}
    assert has_login_cookie(cookies)
    assert cookie_header(cookies) == "other=x; passport_auth_status=true; sessionid_ss=abc"
    assert not has_login_cookie({"ttwid": "anonymous"})
    assert not has_login_cookie({"passport_auth_status": "0", "uid_tt": "device-only"})


def test_ca_bundle_is_prepared_on_ascii_path():
    path = ServerManager.prepare_ca_bundle()
    assert path.exists()
    assert path.stat().st_size > 100_000
    assert all(ord(character) < 128 for character in str(path))
