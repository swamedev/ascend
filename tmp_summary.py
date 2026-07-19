from dataclasses import dataclass, field
from typing import List


class AssessmentResult:
    ...


class CompetencyUpdate:
    ...


class MissionResult:
    ...


class JourneyResult:
    ...


@dataclass
class ExecutionReport:
    ...

    def summary(self) -> str:
        lines = []
        for jr in self.journey_results:
            status = "✔" if jr.completed else "✘"
            lines.append(f"{status} Journey: {jr.journey_id}")
            for mr in jr.mission_results:
                m_status = "✔" if mr.completed else "✘"
                lines.append(f"  {m_status} Mission: {mr.mission_id}")
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

        if self.total_xp > 0 and not any(
            cu.new_level > cu.previous_level
            for jr in self.journey_results
            for mr in jr.mission_results
            for cu in mr.competency_updates
        ):
            pass

        for ach in self.achievements_earned:
            lines.append(f"  Achievement unlocked: {ach}")

        if self.total_xp > 0:
            lines.append(f"Total XP: +{self.total_xp}")

        level_jumps = set()
        for jr in self.journey_results:
            for mr in jr.mission_results:
                for cu in mr.competency_updates:
                    if cu.new_level > cu.previous_level:
                        level_jumps.add(cu.new_level)
        for lv in sorted(level_jumps):
            lines.append(f"Level Up! ({lv})")

        if self.success:
            lines.append("Journey completed successfully.")
        else:
            for err in self.errors:
                lines.append(f"Error: {err}")
            lines.append("Journey completed with errors.")

        return "\n".join(lines)
