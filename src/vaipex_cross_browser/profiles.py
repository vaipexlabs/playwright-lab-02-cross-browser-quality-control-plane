from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CompatibilityProfile:
    name: str
    purpose: str
    width: int
    height: int
    locale: str
    timezone_id: str
    touch: bool = False
    reduced_motion: str = "no-preference"
    device_scale_factor: float = 1

    def context_options(self) -> dict[str, object]:
        options: dict[str, object] = {
            "viewport": {"width": self.width, "height": self.height},
            "locale": self.locale,
            "timezone_id": self.timezone_id,
            "reduced_motion": self.reduced_motion,
            "device_scale_factor": self.device_scale_factor,
        }
        if self.touch:
            options["has_touch"] = True
        return options


PROFILES = {
    "desktop-standard": CompatibilityProfile(
        name="desktop-standard",
        purpose="Primary desktop release signal",
        width=1440,
        height=900,
        locale="en-US",
        timezone_id="America/New_York",
    ),
    "desktop-compact": CompatibilityProfile(
        name="desktop-compact",
        purpose="Constrained desktop and alternate English locale",
        width=1024,
        height=768,
        locale="en-GB",
        timezone_id="Europe/London",
    ),
    "mobile-touch": CompatibilityProfile(
        name="mobile-touch",
        purpose="Narrow viewport and touch-oriented navigation",
        width=390,
        height=844,
        locale="en-US",
        timezone_id="America/Los_Angeles",
        touch=True,
        device_scale_factor=3,
    ),
    "french-locale": CompatibilityProfile(
        name="french-locale",
        purpose="Locale-sensitive formatting and European timezone",
        width=1280,
        height=800,
        locale="fr-FR",
        timezone_id="Europe/Paris",
    ),
    "reduced-motion": CompatibilityProfile(
        name="reduced-motion",
        purpose="Reduced-motion operating-system preference",
        width=1280,
        height=800,
        locale="en-US",
        timezone_id="UTC",
        reduced_motion="reduce",
    ),
}
DEFAULT_PROFILE = "desktop-standard"


def get_profile(name: str) -> CompatibilityProfile:
    try:
        return PROFILES[name]
    except KeyError as error:
        supported = ", ".join(PROFILES)
        raise ValueError(
            f"Unknown profile '{name}'. Choose one of: {supported}."
        ) from error
