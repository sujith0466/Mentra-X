"""
Mentra X — Proactive Opportunity Recommendation & Notification Engine (Phase 10 Module 6)

Synthesizes daily/weekly/monthly opportunity feeds and generates proactive notifications
for high matches, approaching deadlines, skill gap closures, and resume tips.
"""

from datetime import datetime
from typing import List
from backend.services.opportunity.dto import MatchedOpportunityDTO, OpportunityNotificationDTO


class OpportunityRecommendationEngine:
    """
    Ranks opportunities by career impact, urgency, and readiness,
    and generates high-priority actionable notifications.
    """

    def rank_opportunities(
        self,
        matches: List[MatchedOpportunityDTO]
    ) -> List[MatchedOpportunityDTO]:
        # Sort primarily by match percentage descending, then readiness level
        return sorted(
            matches,
            key=lambda m: (m.match_percentage, 1 if m.readiness_level == "IMMEDIATE_READY" else 0),
            reverse=True
        )

    def generate_proactive_notifications(
        self,
        ranked_matches: List[MatchedOpportunityDTO]
    ) -> List[OpportunityNotificationDTO]:
        notifications: List[OpportunityNotificationDTO] = []
        now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M")

        for idx, item in enumerate(ranked_matches):
            opp = item.opportunity
            if item.match_percentage >= 88.0:
                notifications.append(
                    OpportunityNotificationDTO(
                        notification_id=f"notif-match-{opp.opportunity_id}",
                        title=f"High Opportunity Match ({item.match_percentage:.1f}%)",
                        message=f"You are strongly qualified for {opp.title} at {opp.organization}. {item.readiness_level.replace('_', ' ')}.",
                        category="NEW_MATCH",
                        action_url="/student/opportunities",
                        created_at=now_str
                    )
                )

            if item.skill_gap and len(item.skill_gap.missing_skills) > 0:
                notifications.append(
                    OpportunityNotificationDTO(
                        notification_id=f"notif-gap-{opp.opportunity_id}",
                        title="Skill Gap Bridge Ready",
                        message=f"Complete your {item.skill_gap.estimated_readiness_days}-day bridge to reach {item.skill_gap.expected_match_after_remediation_pct:.1f}% match for {opp.organization}.",
                        category="SKILL_GAP_CLOSED",
                        action_url="/student/opportunities",
                        created_at=now_str
                    )
                )

            if item.resume_readiness and item.resume_readiness.ats_score < 80.0:
                notifications.append(
                    OpportunityNotificationDTO(
                        notification_id=f"notif-res-{opp.opportunity_id}",
                        title="Resume Improvement Tip",
                        message=f"Add missing keywords ({', '.join(item.resume_readiness.missing_keywords[:2])}) to increase your selection chances.",
                        category="RESUME_TIP",
                        action_url="/student/career/resume",
                        created_at=now_str
                    )
                )

            # Limit notifications to top 5 most critical
            if len(notifications) >= 5:
                break

        return notifications
