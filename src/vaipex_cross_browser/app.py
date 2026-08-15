from __future__ import annotations

import hashlib
import os
from dataclasses import asdict, dataclass
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

PACKAGE_ROOT = Path(__file__).parent


@dataclass(frozen=True)
class Experience:
    id: str
    name: str
    location: str
    category: str
    duration: str
    price: int
    description: str
    accent: str


EXPERIENCES = (
    Experience(
        id="design-sprint",
        name="Copenhagen Design Sprint",
        location="Copenhagen, Denmark",
        category="Design",
        duration="3 days",
        price=640,
        description=(
            "Prototype an inclusive product experience with a small design team."
        ),
        accent="violet",
    ),
    Experience(
        id="platform-summit",
        name="Lisbon Platform Summit",
        location="Lisbon, Portugal",
        category="Engineering",
        duration="2 days",
        price=890,
        description="Exchange practical platform patterns with engineering leaders.",
        accent="blue",
    ),
    Experience(
        id="reliability-retreat",
        name="Kyoto Reliability Retreat",
        location="Kyoto, Japan",
        category="Reliability",
        duration="4 days",
        price=1120,
        description=(
            "Practice incident leadership and sustainable reliability planning."
        ),
        accent="green",
    ),
)
EXPERIENCE_BY_ID = {experience.id: experience for experience in EXPERIENCES}


class BookingRequest(BaseModel):
    experience_ids: list[str] = Field(min_length=1, max_length=len(EXPERIENCES))
    traveler_name: str = Field(min_length=2, max_length=80)
    traveler_email: str = Field(
        min_length=3,
        max_length=254,
        pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
    )


class BookingResponse(BaseModel):
    booking_id: str
    status: str
    total: int
    experience_count: int


app = FastAPI(title="Vaipex Responsive Lab", version="0.1.0")
app.mount("/static", StaticFiles(directory=PACKAGE_ROOT / "static"), name="static")
templates = Jinja2Templates(directory=PACKAGE_ROOT / "templates")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "vaipex-responsive-lab"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"experiences": EXPERIENCES},
    )


@app.get("/api/experiences")
def list_experiences() -> dict[str, list[dict[str, object]]]:
    return {"experiences": [asdict(experience) for experience in EXPERIENCES]}


@app.post("/api/bookings", response_model=BookingResponse)
def create_booking(booking: BookingRequest) -> BookingResponse:
    if len(set(booking.experience_ids)) != len(booking.experience_ids):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Each experience can appear only once.",
        )

    unknown_ids = sorted(set(booking.experience_ids) - EXPERIENCE_BY_ID.keys())
    if unknown_ids:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Unknown experience: {unknown_ids[0]}",
        )

    normalized_ids = sorted(booking.experience_ids)
    total = sum(EXPERIENCE_BY_ID[item_id].price for item_id in normalized_ids)
    booking_source = f"{booking.traveler_email.casefold()}:{','.join(normalized_ids)}"
    suffix = hashlib.sha256(booking_source.encode()).hexdigest()[:6].upper()
    return BookingResponse(
        booking_id=f"VXP-{suffix}",
        status="confirmed",
        total=total,
        experience_count=len(normalized_ids),
    )


@app.post("/api/test/reset")
def reset_test_state() -> dict[str, str]:
    if os.getenv("VAIPEX_TEST_MODE") != "1":
        raise HTTPException(status_code=403, detail="Test controls are disabled")
    return {"status": "reset"}
