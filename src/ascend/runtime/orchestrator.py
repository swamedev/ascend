from ascend.domain.builder import Builder
from ascend.domain.events import DomainEvent

from .assessment.pipeline import AssessmentPipeline
from .competency.engine import CompetencyEngine
from .context import RuntimeContext
from .hooks import RuntimeHooks
from .report import ExecutionReport, JourneyResult
from .runners.challenge_runner import ChallengeRunner
from .runners.journey_runner import JourneyRunner
from .runners.mission_runner import MissionRunner


class RuntimeOrchestrator:
    def __init__(self) -> None:
        self._challenge_runner = ChallengeRunner()
        self._competency_engine = CompetencyEngine()
        self._assessment_pipeline = AssessmentPipeline()
        self._mission_runner = MissionRunner(
            assessment_pipeline=self._assessment_pipeline,
            competency_engine=self._competency_engine,
            challenge_runner=self._challenge_runner,
        )
        self._journey_runner = JourneyRunner(
            mission_runner=self._mission_runner,
        )

    def run(self, context: RuntimeContext) -> ExecutionReport:
        builder = context.builder
        journey_results: list[JourneyResult] = []
        total_xp = 0
        missions_completed = 0
        competencies_unlocked: list[str] = []
        achievements_earned: list[str] = []
        errors: list[str] = []

        for journey in context.package.journeys:
            try:
                j_result = self._journey_runner.run(journey, builder, context)
                journey_results.append(j_result)
                for mr in j_result.mission_results:
                    if mr.competency_updates:
                        for cu in mr.competency_updates:
                            total_xp += cu.xp_gained
                            if cu.unlocked:
                                competencies_unlocked.append(cu.competency_id)
                            achievements_earned.extend(cu.achievements_unlocked)
                    if mr.completed:
                        missions_completed += 1
            except Exception as e:
                errors.append(f"Journey '{journey.id}' failed: {e}")
                journey_results.append(
                    JourneyResult(
                        journey_id=journey.id,
                        started=False,
                        completed=False,
                    )
                )

        success = len(errors) == 0

        return ExecutionReport(
            success=success,
            package_id=context.package.id,
            builder_username=builder.username,
            duration=0.0,
            journeys_completed=sum(1 for j in journey_results if j.completed),
            missions_completed=missions_completed,
            total_xp=total_xp,
            competencies_unlocked=competencies_unlocked,
            achievements_earned=achievements_earned,
            journey_results=journey_results,
            errors=errors,
        )
