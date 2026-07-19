from ascend.application.commands.unlock_competency import UnlockCompetency
from ascend.application.dto.builder_dto import BuilderDTO
from ascend.application.exceptions import BuilderNotFound
from ascend.application.interfaces.event_bus import EventBus
from ascend.application.interfaces.repositories import (
    BuilderRepository,
    CompetencyRepository,
)
from ascend.domain.competency import Competency


class CompetencyService:
    def __init__(
        self,
        builder_repo: BuilderRepository,
        competency_repo: CompetencyRepository,
        event_bus: EventBus,
    ) -> None:
        self._builder_repo = builder_repo
        self._competency_repo = competency_repo
        self._event_bus = event_bus

    def unlock_competency(self, command: UnlockCompetency) -> BuilderDTO:
        builder = self._builder_repo.get(command.builder_id)
        if not builder:
            raise BuilderNotFound(f"Builder {command.builder_id} not found")
        competency = Competency(
            name=command.name,
            description=command.description,
            level=command.level,
            criteria=command.criteria,
        )
        builder.add_competency(competency)
        self._builder_repo.save(builder)
        self._competency_repo.save(competency)
        self._event_bus.publish(builder.events)
        return BuilderDTO(
            id=builder.id,
            username=builder.username,
            level=builder.level,
            xp=builder.xp,
            competency_count=len(builder.competencies),
            achievement_count=len(builder.achievements),
            active_mission_count=len(builder.active_missions),
        )
