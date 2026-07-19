from ascend.application.commands.create_builder import CreateBuilder
from ascend.application.dto.builder_dto import BuilderDTO
from ascend.application.exceptions import BuilderNotFound
from ascend.application.interfaces.event_bus import EventBus
from ascend.application.interfaces.repositories import BuilderRepository
from ascend.domain.builder import Builder


class BuilderService:
    def __init__(self, repo: BuilderRepository, event_bus: EventBus) -> None:
        self._repo = repo
        self._event_bus = event_bus

    def create_builder(self, command: CreateBuilder) -> BuilderDTO:
        builder = Builder(username=command.username)
        self._repo.save(builder)
        self._event_bus.publish(builder.events)
        return self._to_dto(builder)

    def get_builder(self, builder_id: str) -> BuilderDTO:
        builder = self._repo.get(builder_id)
        if not builder:
            raise BuilderNotFound(f"Builder {builder_id} not found")
        return self._to_dto(builder)

    def gain_xp(self, builder_id: str, amount: int) -> BuilderDTO:
        builder = self._repo.get(builder_id)
        if not builder:
            raise BuilderNotFound(f"Builder {builder_id} not found")
        builder.gain_xp(amount)
        self._repo.save(builder)
        self._event_bus.publish(builder.events)
        return self._to_dto(builder)

    def _to_dto(self, builder: Builder) -> BuilderDTO:
        return BuilderDTO(
            id=builder.id,
            username=builder.username,
            level=builder.level,
            xp=builder.xp,
            competency_count=len(builder.competencies),
            achievement_count=len(builder.achievements),
            active_mission_count=len(builder.active_missions),
        )
