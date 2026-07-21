"""CompleteMissionUseCase — business logic for mission completion.

Extracted from api/routers/mission.py per A1.1 (OPERAÇÃO AURORA).
Zero HTTP knowledge. Receives RuntimeAdapter, calls public methods only.
"""

from datetime import datetime
from typing import Any

from ascend.adapter.runtime_adapter import RuntimeAdapter


class CompleteMissionUseCase:
    def __init__(self, adapter: RuntimeAdapter) -> None:
        self._adapter = adapter

    def execute(
        self, builder_id: str, mission_id: str
    ) -> dict[str, Any]:
        evidence_records = self._adapter._evidence_repo.list_by_builder_and_mission(builder_id, mission_id)
        mission_evidence = [{"id": e.id, "missionId": e.mission_id} for e in evidence_records]

        completed = False
        xp_earned = 0
        evidence_accepted = 0
        evidence_rejected = 0
        competencies_advanced: list[str] = []

        if mission_evidence:
            evidence = mission_evidence[0]
            assess_result = self._adapter.complete_assessment(
                evidence_id=evidence["id"],
                score=0.85,
                feedback="Auto-assessed",
                reviewer="system",
            )

            if assess_result.get("success") and assess_result["data"].get("passed"):
                passed = True
                evidence_accepted = 1
            else:
                passed = False
                evidence_rejected = 1

            if passed:
                completed = True

                mission_result = self._adapter.get_mission(mission_id)
                mission_data = mission_result.get("data", {})
                xp_reward = mission_data.get("xpReward", 100) if mission_data else 100

                self._adapter.award_xp(builder_id, xp_reward)
                xp_earned = xp_reward

                self._adapter.mark_mission_completed(mission_id)

                if "python" in mission_id.lower():
                    self._adapter.unlock_competency(
                        builder_id=builder_id,
                        name="Python Basics",
                        description="Fundamentos da programação Python",
                    )
                    competencies_advanced.append("Python Basics")

                completed_count = self._adapter.count_completed_missions(builder_id)
                is_first = completed_count == 0

                if is_first:
                    self._adapter.grant_builder_achievement(
                        builder_id=builder_id,
                        name="First Mission",
                        description="Complete your first mission",
                        achievement_id="ach-first-mission",
                    )

        return {
            "missionId": mission_id,
            "builderId": builder_id,
            "completed": completed,
            "xpEarned": xp_earned,
            "evidenceAccepted": evidence_accepted,
            "evidenceRejected": evidence_rejected,
            "competenciesAdvanced": competencies_advanced,
            "completedAt": datetime.now().isoformat() if completed else None,
        }
