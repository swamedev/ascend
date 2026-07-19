from ascend.domain.builder import Builder

from ..context import RuntimeContext
from ..models import RuntimeJourney
from ..report import JourneyResult, MissionResult
from .challenge_runner import ChallengeRunner
from .mission_runner import MissionRunner


class JourneyRunner:
    def __init__(self, mission_runner: MissionRunner):
        self._mission_runner = mission_runner

    def run(
        self, journey: RuntimeJourney, builder: Builder, context: RuntimeContext
    ) -> JourneyResult:
        context.hooks.before_journey(journey.id, context)

        mission_results: list[MissionResult] = []
        for mission in journey.missions:
            prereqs_met = all(
                any(
                    m.id == prereq and m.completed
                    for m in mission_results
                )
                for prereq in mission.prerequisites
            )
            if not prereqs_met:
                continue

            m_result = self._mission_runner.run(mission, builder, context)
            mission_results.append(m_result)

        completed = sum(1 for m in mission_results if m.completed)
        all_done = completed == len(journey.missions)

        context.hooks.after_journey(journey.id, context)

        return JourneyResult(
            journey_id=journey.id,
            started=len(mission_results) > 0,
            completed=all_done,
            mission_results=mission_results,
        )
