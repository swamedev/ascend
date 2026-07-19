from ..models import RuntimeAchievement, RuntimeCompetency, RuntimeMission, RuntimePackage
from ..report import AssessmentResult, CompetencyUpdate


class CompetencyEngine:
    def process(
        self,
        result: AssessmentResult,
        mission: RuntimeMission,
        package: RuntimePackage,
        current_xp: int,
        current_level: int,
        unlocked_competency_ids: set[str],
        earned_achievement_ids: set[str],
    ) -> CompetencyUpdate:
        xp_gained = mission.xp if result.passed else 0
        new_xp = current_xp + xp_gained
        new_level = (new_xp // 500) + 1

        unlocked = []
        for cid in mission.competencies:
            if cid not in unlocked_competency_ids and result.passed:
                comp_def = package.competencies.get(cid)
                if comp_def and result.percentage >= comp_def.mastery_threshold:
                    unlocked.append(cid)

        achievements_earned = []
        for aid, ach_def in package.achievements.items():
            if aid in earned_achievement_ids:
                continue
            if self._check_achievement_criteria(ach_def, unlocked, result):
                achievements_earned.append(aid)

        return CompetencyUpdate(
            competency_id=mission.competencies[0] if mission.competencies else "",
            unlocked=len(unlocked) > 0,
            xp_gained=xp_gained,
            previous_xp=current_xp,
            new_xp=new_xp,
            previous_level=current_level,
            new_level=new_level,
            achievements_unlocked=achievements_earned,
        )

    def _check_achievement_criteria(
        self,
        ach_def: RuntimeAchievement,
        unlocked_competencies: list[str],
        result: AssessmentResult,
    ) -> bool:
        for criterion in ach_def.criteria:
            if "completar" in criterion.lower():
                for cid in unlocked_competencies:
                    if cid in criterion.lower():
                        return True
                return False
            if "assessment" in criterion.lower() and result.passed:
                return True
            return True
        return True
