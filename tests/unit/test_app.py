from fastapi.testclient import TestClient

from vaipex_cross_browser.app import app


def test_health_contract() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "vaipex-responsive-lab",
    }


def test_homepage_exposes_responsive_test_contract() -> None:
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert "Vaipex Explorer" in response.text
    assert 'data-testid="mobile-menu-toggle"' in response.text
    assert response.text.count('data-testid="experience-card"') == 3
    assert 'data-testid="plan-summary"' in response.text


def test_experience_catalog_is_deterministic() -> None:
    with TestClient(app) as client:
        response = client.get("/api/experiences")

    assert response.status_code == 200
    experiences = response.json()["experiences"]
    assert [experience["id"] for experience in experiences] == [
        "design-sprint",
        "platform-summit",
        "reliability-retreat",
    ]
    assert sum(experience["price"] for experience in experiences) == 2650


def test_booking_is_confirmed_with_deterministic_reference() -> None:
    booking = {
        "experience_ids": ["platform-summit", "design-sprint"],
        "traveler_name": "Vaipex Developer",
        "traveler_email": "developer@vaipex.io",
    }
    with TestClient(app) as client:
        first = client.post("/api/bookings", json=booking)
        second = client.post("/api/bookings", json=booking)

    assert first.status_code == 200
    assert first.json() == second.json()
    assert first.json()["booking_id"].startswith("VXP-")
    assert first.json()["status"] == "confirmed"
    assert first.json()["total"] == 1530
    assert first.json()["experience_count"] == 2


def test_booking_rejects_unknown_experience() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/api/bookings",
            json={
                "experience_ids": ["unknown"],
                "traveler_name": "Vaipex Developer",
                "traveler_email": "developer@vaipex.io",
            },
        )

    assert response.status_code == 422
    assert response.json()["detail"] == "Unknown experience: unknown"
