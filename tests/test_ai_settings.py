from app.secure_store import save_ai_configuration


class FakeSettings:
    def __init__(self):
        self.secret = None
        self.values = {}

    def set_secret(self, key, value):
        self.secret = (key, value)

    def update(self, **values):
        self.values.update(values)


def test_connection_test_configuration_is_fully_persisted():
    store = FakeSettings()

    save_ai_configuration(
        store,
        "secret-key",
        " https://api.example.com/v1 ",
        " model-name ",
        0.6,
        "analysis prompt",
        "rewrite prompt",
    )

    assert store.secret == ("ai_api_key", "secret-key")
    assert store.values == {
        "ai_base_url": "https://api.example.com/v1",
        "ai_model": "model-name",
        "ai_temperature": 0.6,
        "ai_timeout": 90,
        "analysis_prompt": "analysis prompt",
        "rewrite_prompt": "rewrite prompt",
    }


def test_blank_key_keeps_existing_saved_secret():
    store = FakeSettings()

    save_ai_configuration(store, "", "https://api.example.com/v1", "model", 0.7, "a", "r")

    assert store.secret is None
