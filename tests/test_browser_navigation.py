from app.douyin_browser import should_retry_destroyed_context


def test_navigation_during_search_is_retryable_before_last_round():
    assert should_retry_destroyed_context("Execution context was destroyed", 1)
    assert not should_retry_destroyed_context("Execution context was destroyed", 6)
    assert not should_retry_destroyed_context("Target page has been closed", 1)
