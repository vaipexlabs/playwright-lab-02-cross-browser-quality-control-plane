from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class Traveler:
    name: str
    email: str


@dataclass(frozen=True)
class AutomationSettings:
    base_url: str
    timeout_ms: int
    traveler: Traveler

    @classmethod
    def from_environment(cls, default_base_url: str) -> AutomationSettings:
        base_url = os.getenv("VAIPEX_BASE_URL", default_base_url).strip().rstrip("/")
        parsed_url = urlparse(base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("VAIPEX_BASE_URL must be an absolute HTTP or HTTPS URL.")

        raw_timeout = os.getenv("VAIPEX_EXPECT_TIMEOUT_MS", "5000")
        try:
            timeout_ms = int(raw_timeout)
        except ValueError as error:
            raise ValueError("VAIPEX_EXPECT_TIMEOUT_MS must be an integer.") from error
        if timeout_ms <= 0:
            raise ValueError("VAIPEX_EXPECT_TIMEOUT_MS must be greater than zero.")

        traveler = Traveler(
            name=os.getenv("VAIPEX_TRAVELER_NAME", "Vaipex Developer").strip(),
            email=os.getenv("VAIPEX_TRAVELER_EMAIL", "developer@vaipex.io").strip(),
        )
        if not traveler.name or not traveler.email:
            raise ValueError("Traveler values must not be empty.")

        return cls(base_url=base_url, timeout_ms=timeout_ms, traveler=traveler)
