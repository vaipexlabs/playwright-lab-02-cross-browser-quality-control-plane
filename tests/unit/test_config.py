import pytest

from tests.config import AutomationSettings


def test_default_settings_use_local_reference_target(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    for variable in (
        "VAIPEX_BASE_URL",
        "VAIPEX_EXPECT_TIMEOUT_MS",
        "VAIPEX_TRAVELER_NAME",
        "VAIPEX_TRAVELER_EMAIL",
    ):
        monkeypatch.delenv(variable, raising=False)

    settings = AutomationSettings.from_environment("http://127.0.0.1:8123")

    assert settings.base_url == "http://127.0.0.1:8123"
    assert settings.timeout_ms == 5000
    assert settings.traveler.name == "Vaipex Developer"
    assert settings.traveler.email == "developer@vaipex.io"


def test_settings_reject_invalid_target(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VAIPEX_BASE_URL", "not-a-url")

    with pytest.raises(ValueError, match="absolute HTTP or HTTPS URL"):
        AutomationSettings.from_environment("http://127.0.0.1:8123")


def test_settings_reject_nonpositive_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("VAIPEX_EXPECT_TIMEOUT_MS", "0")

    with pytest.raises(ValueError, match="greater than zero"):
        AutomationSettings.from_environment("http://127.0.0.1:8123")
