from ascend.application.commands.start_mission import StartMission
from ascend.application.commands.submit_evidence import SubmitEvidence
from ascend.application.dto.mission_dto import MissionDTO
from ascend.application.dto.evidence_dto import EvidenceDTO
from ascend.application.exceptions import BuilderNotFound, MissionNotFound
from ascend.application.interfaces.event_bus import EventBus
from ascend.application.interfaces.repositories import (
    BuilderRepository,
    MissionRepository,
    EvidenceRepository,
)
from ascend.domain.builder import Builder
from ascend.domain.evidence import Evidence
from ascend.domain.mission import Mission


class MissionService:
    def __init__(
        self,
        builder_repo: BuilderRepository,
        mission_repo: MissionRepository,
        evidence_repo: EvidenceRepository,
        event_bus: EventBus,
    ) -> None:
        self._builder_repo = builder_repo
        self._mission_repo = mission_repo
        self._evidence_repo = evidence_repo
        self._event_bus = event_bus

    def start_mission(self, command: StartMission) -> MissionDTO:
        builder = self._builder_repo.get(command.builder_id)
        if not builder:
            raise BuilderNotFound(f"Builder {command.builder_id} not found")
        mission = self._mission_repo.get(command.mission_id)
        if not mission:
            raise MissionNotFound(f"Mission {command.mission_id} not found")
        builder.start_mission(mission)
        self._builder_repo.save(builder)
        self._mission_repo.save(mission)
        self._event_bus.publish(builder.events)
        return self._mission_to_dto(mission)

    def submit_evidence(self, command: SubmitEvidence) -> EvidenceDTO:
        builder = self._builder_repo.get(command.builder_id)
        if not builder:
            raise BuilderNotFound(f"Builder {command.builder_id} not found")
        mission = self._mission_repo.get(command.mission_id)
        if not mission:
            raise MissionNotFound(f"Mission {command.mission_id} not found")
        evidence = Evidence(
            artifact=command.artifact,
            type=command.evidence_type,
            mission_id=command.mission_id,
        )
        builder.submit_evidence(evidence, mission)
        self._builder_repo.save(builder)
        self._mission_repo.save(mission)
        self._evidence_repo.save(evidence)
        self._event_bus.publish(builder.events)
        return self._evidence_to_dto(evidence)

    def get_mission(self, mission_id: str) -> MissionDTO:
        mission = self._mission_repo.get(mission_id)
        if not mission:
            raise MissionNotFound(f"Mission {mission_id} not found")
        return self._mission_to_dto(mission)

    def _mission_to_dto(self, mission: Mission) -> MissionDTO:
        return MissionDTO(
            id=mission.id,
            title=mission.title,
            objective=mission.objective,
            difficulty=mission.difficulty,
            xp_reward=mission.xp_reward,
            status=mission.status.value,
        )

    def _evidence_to_dto(self, evidence: Evidence) -> EvidenceDTO:
        return EvidenceDTO(
            id=evidence.id,
            artifact=evidence.artifact,
            type=evidence.type.value,
            status=evidence.status.value,
            builder_id=evidence.builder_id,
            submitted_at=(
                evidence.submitted_at.isoformat()
                if evidence.submitted_at
                else ""
            ),
        )
