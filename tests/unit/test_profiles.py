import pytest

from vaipex_cross_browser.profiles import DEFAULT_PROFILE, PROFILES, get_profile


def test_profile_catalog_is_intentional() -> None:
    assert tuple(PROFILES) == (
        "desktop-standard",
        "desktop-compact",
        "mobile-touch",
        "french-locale",
        "reduced-motion",
    )
    assert DEFAULT_PROFILE == "desktop-standard"


def test_mobile_profile_declares_touch_and_narrow_viewport() -> None:
    profile = get_profile("mobile-touch")

    assert profile.touch is True
    assert profile.width == 390
    assert profile.context_options()["has_touch"] is True
    assert profile.context_options()["device_scale_factor"] == 3


def test_locale_profile_declares_browser_locale_and_timezone() -> None:
    profile = get_profile("french-locale")

    assert profile.locale == "fr-FR"
    assert profile.timezone_id == "Europe/Paris"


def test_unknown_profile_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown profile 'unsupported'"):
        get_profile("unsupported")
