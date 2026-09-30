from datetime import datetime, timedelta

from app.douyin_browser import SearchPolicy, cookie_header_from_playwright, cookie_records_from_header, launch_persistent_browser, playwright_cookies_logged_in


class FakeChromium:
    def __init__(self, edge_works=True):
        self.edge_works = edge_works
        self.calls = []

    def launch_persistent_context(self, path, **options):
        self.calls.append((path, options))
        if options.get("channel") == "msedge" and not self.edge_works:
            raise RuntimeError("Edge missing")
        return {"browser": options.get("channel", "chromium")}


class FakePlaywright:
    def __init__(self, edge_works=True):
        self.chromium = FakeChromium(edge_works)


def test_playwright_cookie_helpers_only_use_douyin_domain():
    cookies = [
        {"name": "sessionid_ss", "value": "real", "domain": ".douyin.com"},
        {"name": "other", "value": "ignore", "domain": ".example.com"},
    ]
    assert playwright_cookies_logged_in(cookies)
    assert cookie_header_from_playwright(cookies) == "sessionid_ss=real"


def test_saved_cookie_header_can_seed_persistent_browser():
    records = cookie_records_from_header("sessionid_ss=real; passport_auth_status=1; broken")
    assert records == [
        {"name": "sessionid_ss", "value": "real", "domain": ".douyin.com", "path": "/"},
        {"name": "passport_auth_status", "value": "1", "domain": ".douyin.com", "path": "/"},
    ]


def test_search_policy_applies_interval_and_circuit_breaker(tmp_path):
    policy = SearchPolicy(tmp_path)
    policy.record_started()
    seconds, reason = policy.seconds_until_allowed()
    assert 1 <= seconds <= policy.MIN_SEARCH_INTERVAL_SECONDS
    assert "排队" in reason

    policy.record_abnormal()
    seconds, reason = policy.seconds_until_allowed()
    assert seconds > 60
    assert "保护账号" in reason

    policy.record_success()
    state = policy._load()
    assert "cooldown_until" not in state


def test_gateway_failure_uses_shorter_cooldown(tmp_path):
    policy = SearchPolicy(tmp_path)
    policy.record_gateway_failure()
    seconds, reason = policy.seconds_until_allowed()
    assert 60 < seconds <= policy.GATEWAY_COOLDOWN_MINUTES * 60
    assert "保护账号" in reason


def test_expired_cooldown_does_not_block(tmp_path):
    policy = SearchPolicy(tmp_path)
    policy._save({"cooldown_until": (datetime.now() - timedelta(minutes=1)).isoformat()})
    assert policy.seconds_until_allowed() == (0, "")


def test_browser_launcher_prefers_edge(tmp_path):
    playwright = FakePlaywright(edge_works=True)
    context, name = launch_persistent_browser(playwright, tmp_path)
    assert name == "Microsoft Edge"
    assert context["browser"] == "msedge"
    assert len(playwright.chromium.calls) == 1
    assert playwright.chromium.calls[0][1]["ignore_default_args"] == ["--no-sandbox"]


def test_browser_launcher_falls_back_to_bundled_chromium(tmp_path):
    messages = []
    playwright = FakePlaywright(edge_works=False)
    context, name = launch_persistent_browser(playwright, tmp_path, messages.append)
    assert name == "内置 Chromium"
    assert context["browser"] == "chromium"
    assert len(playwright.chromium.calls) == 2
    assert "内置浏览器" in messages[0]
