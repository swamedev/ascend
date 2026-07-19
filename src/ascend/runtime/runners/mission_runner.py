from ascend.domain.builder import Builder
from ascend.domain.competency import Competency
from ascend.domain.events import (
    AchievementEarned,
    AssessmentCompleted,
    CompetencyUnlocked,
    EvidenceSubmitted,
    MissionStarted,
)
from ascend.domain.evidence import Evidence, EvidenceType
from ascend.domain.mission import Mission, MissionStatus

from ..assessment.pipeline import AssessmentPipeline
from ..competency.engine import CompetencyEngine
from ..context import RuntimeContext
from ..models import RuntimeMission
from ..report import AssessmentResult, CompetencyUpdate, MissionResult
from .challenge_runner import ChallengeRunner


class MissionRunner:
    def __init__(
        self,
        assessment_pipeline: AssessmentPipeline,
        competency_engine: CompetencyEngine,
        challenge_runner: ChallengeRunner,
    ):
        self._assessment = assessment_pipeline
        self._competency = competency_engine
        self._challenge = challenge_runner

    def run(
        self, mission: RuntimeMission, builder: Builder, context: RuntimeContext
    ) -> MissionResult:
        context.hooks.before_mission(mission.id, context)

        domain_mission = Mission(mission.title)
        domain_mission.start()
        context.event_collector.collect(
            MissionStarted(domain_mission.id, builder.id)
        )

        challenge_desc = self._challenge.open(mission, context)
        evidence_text = self._challenge.collect_evidence(mission, context)
        evidence_submitted = bool(evidence_text.strip()) if evidence_text else False

        if evidence_submitted:
            domain_evidence = Evidence(
                artifact=evidence_text,
                type=EvidenceType.CODE,
            )
            domain_evidence.submit(builder.id)
            domain_mission.submit(domain_evidence)
            context.event_collector.collect(
                EvidenceSubmitted(domain_evidence.id, domain_mission.id, builder.id)
            )

        rubric = context.package.rubrics.get(mission.rubric_id) if mission.rubric_id else None
        context.hooks.before_assessment(mission.id, context)

        assessment_result = self._assessment.run(
            evidence_text=evidence_text,
            rubric=rubric,
            mission_id=mission.id,
        )
        context.event_collector.collect(
            AssessmentCompleted(domain_mission.id, mission.id, assessment_result.percentage)
        )
        context.hooks.after_assessment(mission.id, context)

        comp_update = self._competency.process(
            result=assessment_result,
            mission=mission,
            package=context.package,
            current_xp=builder.xp,
            current_level=builder.level,
            unlocked_competency_ids=set(),
            earned_achievement_ids=set(),
        )

        if comp_update.xp_gained > 0:
            builder.add_xp(comp_update.xp_gained)

        for cid in mission.competencies:
            if cid not in [c.name for c in builder.competencies]:
                comp_def = context.package.competencies.get(cid)
                if comp_def:
                    c = Competency(
                        name=comp_def.id,
                        description=comp_def.description,
                        level=comp_update.new_level - builder.level + 1,
                    )
                    builder.add_competency(c)
                    context.event_collector.collect(
                        CompetencyUnlocked(c.id, builder.id, c.level)
                    )

        for aid in comp_update.achievements_unlocked:
            ach_def = context.package.achievements.get(aid)
            if ach_def:
                from ascend.domain.achievement import Achievement

                a = Achievement(
                    name=ach_def.name,
                    description=ach_def.description,
                )
                builder.earn_achievement(a)
                context.event_collector.collect(
                    AchievementEarned(a.id, builder.id)
                )

        if evidence_submitted:
            domain_mission.complete()

        context.hooks.after_mission(mission.id, context)

        return MissionResult(
            mission_id=mission.id,
            started=True,
            completed=comp_update.xp_gained > 0,
            evidence_submitted=evidence_submitted,
            assessment_result=assessment_result,
            competency_updates=[comp_update],
        )
