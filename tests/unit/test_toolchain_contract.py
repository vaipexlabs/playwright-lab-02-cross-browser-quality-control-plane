import sys

from vaipex_cross_browser import __version__
from vaipex_cross_browser.matrix import SUPPORTED_BROWSER_ENGINES


def test_supported_python_series() -> None:
    assert sys.version_info[:2] == (3, 12)


def test_package_version_is_explicit() -> None:
    assert __version__ == "0.1.0"


def test_all_playwright_engines_are_declared() -> None:
    assert SUPPORTED_BROWSER_ENGINES == ("chromium", "firefox", "webkit")
