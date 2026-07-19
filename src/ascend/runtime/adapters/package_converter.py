from ascend.package_engine.models import (
    AchievementDef,
    CompetencyDef,
    Journey as APSJourney,
    Mission as APSMission,
    Package as APSPackage,
    Rubric,
)

from ..models import (
    RuntimeAchievement,
    RuntimeChallenge,
    RuntimeCompetency,
    RuntimeCriterion,
    RuntimeJourney,
    RuntimeMission,
    RuntimePackage,
    RuntimeRubric,
)


class PackageConverter:
    def convert(self, pkg: APSPackage) -> RuntimePackage:
        journeys = [self._convert_journey(j) for j in pkg.journeys]
        competencies = {
            c.id: self._convert_competency(c) for c in pkg.competencies
        }
        rubrics = {r.id: self._convert_rubric(r) for r in pkg.rubrics}
        achievements = {
            a.id: self._convert_achievement(a) for a in pkg.achievements
        }
        return RuntimePackage(
            id=pkg.id,
            version=pkg.version,
            title=pkg.title,
            description=pkg.description,
            author=pkg.author,
            journeys=journeys,
            competencies=competencies,
            rubrics=rubrics,
            achievements=achievements,
            dependencies=pkg.dependencies,
            capabilities=pkg.capabilities,
        )

    def _convert_journey(self, journey: APSJourney) -> RuntimeJourney:
        missions = [self._convert_mission(m) for m in journey.missions]
        return RuntimeJourney(
            id=journey.id,
            title=journey.title,
            description=journey.description,
            difficulty=journey.difficulty,
            estimated_hours=journey.estimated_hours,
            missions=missions,
            unlocks=journey.unlocks,
        )

    def _convert_mission(self, mission: APSMission) -> RuntimeMission:
        return RuntimeMission(
            id=mission.id,
            title=mission.title,
            description=mission.title,
            difficulty=mission.difficulty,
            estimated_minutes=mission.estimated_minutes,
            xp=mission.xp,
            prerequisites=mission.prerequisites,
            competencies=mission.competencies,
            challenge=RuntimeChallenge(
                type=mission.challenge_type,
                description=mission.challenge_description,
                evidence_required=mission.evidence_required,
                evidence_types=mission.evidence_types,
            ),
            rubric_id=mission.rubric,
        )

    def _convert_competency(self, comp: CompetencyDef) -> RuntimeCompetency:
        return RuntimeCompetency(
            id=comp.id,
            name=comp.name,
            description=comp.description,
            level=comp.level,
            evidence_required=comp.evidence_required,
            mastery_threshold=comp.mastery_threshold,
        )

    def _convert_rubric(self, rubric: Rubric) -> RuntimeRubric:
        criteria = {
            cid: RuntimeCriterion(
                weight=c.weight,
                description=c.description,
            )
            for cid, c in rubric.criteria.items()
        }
        return RuntimeRubric(
            id=rubric.id,
            title=rubric.title,
            criteria=criteria,
        )

    def _convert_achievement(self, ach: AchievementDef) -> RuntimeAchievement:
        return RuntimeAchievement(
            id=ach.id,
            name=ach.name,
            description=ach.description,
            criteria=ach.criteria,
            badge=ach.badge,
        )
