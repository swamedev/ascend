from dataclasses import dataclass, field
from typing import List


@dataclass
class AssessmentResult:
    mission_id: str
    rubric_id: str
    scores: dict[str, int]
    total_score: int
    max_score: int
    percentage: float
    passed: bool
    evidence_text: str = ""


@dataclass
class CompetencyUpdate:
    competency_id: str
    unlocked: bool
    xp_gained: int
    previous_xp: int
    new_xp: int
    previous_level: int
    new_level: int
    achievements_unlocked: List[str]


@dataclass
class MissionResult:
    mission_id: str
    started: bool
    completed: bool
    evidence_submitted: bool
    assessment_result: AssessmentResult | None = None
    competency_updates: List[CompetencyUpdate] = field(default_factory=list)


@dataclass
class JourneyResult:
    journey_id: str
    started: bool
    completed: bool
    mission_results: List[MissionResult] = field(default_factory=list)


@dataclass
class ExecutionReport:
    success: bool
    package_id: str
    builder_username: str
    duration: float
    journeys_completed: int
    missions_completed: int
    total_xp: int
    competencies_unlocked: List[str]
    achievements_earned: List[str]
    journey_results: List[JourneyResult] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def summary(self) -> str:
        lines = []
        for jr in self.journey_results:
            icon = "[OK]" if jr.completed else "[FAIL]"
            lines.append(f"{icon} Journey: {jr.journey_id}")
            for mr in jr.mission_results:
                mic = "[OK]" if mr.completed else "[FAIL]"
                lines.append(f"  {mic} Mission: {mr.mission_id}")
                if mr.completed:
                    lines.append(f"    Challenge completed")
                    if mr.evidence_submitted:
                        lines.append(f"    Evidence accepted")
                    for cu in mr.competency_updates:
                        if cu.unlocked:
                            lines.append(f"    Competency unlocked: {cu.competency_id}")
                        if cu.xp_gained > 0:
                            lines.append(f"    XP +{cu.xp_gained}")
                            if cu.new_level > cu.previous_level:
                                lines.append(f"    Level Up! ({cu.new_level})")
                        for ach in cu.achievements_unlocked:
                            lines.append(f"    Achievement unlocked: {ach}")

        if self.success:
            lines.append("Journey completed successfully.")
        else:
            for err in self.errors:
                lines.append(f"Error: {err}")
            lines.append("Journey completed with errors.")
        return "\n".join(lines)
