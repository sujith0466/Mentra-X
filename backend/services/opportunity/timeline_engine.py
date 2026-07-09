"""
Mentra X — Opportunity Lifecycle Timeline Engine (Phase 10 Module 7)

Tracks opportunities across 9 complete lifecycle stages:
RECOMMENDED, SAVED, INTERESTED, APPLIED, INTERVIEW, ACCEPTED, REJECTED, COMPLETED, EXPIRED
"""

from datetime import datetime
from typing import List, Dict
from backend.services.opportunity.dto import TimelineEntryDTO


VALID_LIFECYCLE_STATUSES = {
    "RECOMMENDED",
    "SAVED",
    "INTERESTED",
    "APPLIED",
    "INTERVIEW",
    "ACCEPTED",
    "REJECTED",
    "COMPLETED",
    "EXPIRED"
}


class OpportunityTimelineEngine:
    """
    Manages student opportunity lifecycle progression and reminders.
    """

    def __init__(self):
        # In-memory store keyed by (user_id, opportunity_id) for stateless demo & resilience
        self._timeline_store: Dict[str, TimelineEntryDTO] = {}

    def get_user_timeline(self, user_id: int) -> List[TimelineEntryDTO]:
        user_entries = [entry for entry in self._timeline_store.values() if entry.user_id == user_id]
        if not user_entries:
            # Provide initial default timeline progression entries for student demo
            now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
            default_entries = [
                TimelineEntryDTO(
                    entry_id="tl-101",
                    user_id=user_id,
                    opportunity_id="opp-swe-google",
                    opportunity_title="Google Software Engineering Summer Internship",
                    organization="Google Core AI",
                    status="SAVED",
                    updated_at=now_str,
                    reminder_note="Application deadline approaches in August 2026. Keep resume ATS >80%."
                ),
                TimelineEntryDTO(
                    entry_id="tl-102",
                    user_id=user_id,
                    opportunity_id="opp-hack-eth",
                    opportunity_title="Global Open Source AI Global Hackathon",
                    organization="Mentra X & OpenSource Consortium",
                    status="APPLIED",
                    updated_at=now_str,
                    reminder_note="Submission checkpoint scheduled for July 28, 2026."
                ),
                TimelineEntryDTO(
                    entry_id="tl-103",
                    user_id=user_id,
                    opportunity_id="opp-cert-aws",
                    opportunity_title="AWS Certified Machine Learning Specialty Fellowship",
                    organization="Amazon Web Services Education",
                    status="INTERESTED",
                    updated_at=now_str,
                    reminder_note="Study sprint active — 100% exam voucher qualification."
                )
            ]
            for entry in default_entries:
                key = f"{user_id}_{entry.opportunity_id}"
                self._timeline_store[key] = entry
            user_entries = default_entries

        return sorted(user_entries, key=lambda e: e.updated_at, reverse=True)

    def update_opportunity_status(
        self,
        user_id: int,
        opportunity_id: str,
        opportunity_title: str,
        organization: str,
        new_status: str,
        reminder_note: str = ""
    ) -> TimelineEntryDTO:
        status_upper = new_status.upper().strip()
        if status_upper not in VALID_LIFECYCLE_STATUSES:
            status_upper = "SAVED"

        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
        key = f"{user_id}_{opportunity_id}"
        entry = TimelineEntryDTO(
            entry_id=f"tl-{user_id}-{opportunity_id}",
            user_id=user_id,
            opportunity_id=opportunity_id,
            opportunity_title=opportunity_title,
            organization=organization,
            status=status_upper,
            updated_at=now_str,
            reminder_note=reminder_note or f"Updated status to {status_upper}"
        )
        self._timeline_store[key] = entry
        return entry
