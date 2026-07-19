from dataclasses import dataclass, field
from typing import List, Optional

import pytest

from ascend.application.commands import (
    CreateBuilder,
    StartMission,
    SubmitEvidence,
    CompleteAssessment,
    UnlockCompetency,
)
from ascend.application.dto import BuilderDTO, MissionDTO, EvidenceDTO
from ascend.application.exceptions import BuilderNotFound, EvidenceRequired, MissionNotFound
from ascend.application.services import (
    AssessmentService,
    BuilderService,
    MissionService,
    CompetencyService,
)
from ascend.domain.builder import Builder
from ascend.domain.mission import Mission
from ascend.domain.evidence import Evidence, EvidenceStatus, EvidenceType
from ascend.domain.competency import Competency
from ascend.domain.events import DomainEvent


@dataclass
class InMemoryBuilderRepo:
    builders: dict = field(default_factory=dict)

    def save(self, builder: Builder) -> None:
        self.builders[builder.id] = builder

    def get(self, builder_id: str) -> Optional[Builder]:
        return self.builders.get(builder_id)

    def get_by_username(self, username: str) -> Optional[Builder]:
        for b in self.builders.values():
            if b.username == username:
                return b
        return None

    def list(self) -> List[Builder]:
        return list(self.builders.values())


@dataclass
class InMemoryMissionRepo:
    missions: dict = field(default_factory=dict)

    def save(self, mission: Mission) -> None:
        self.missions[mission.id] = mission

    def get(self, mission_id: str) -> Optional[Mission]:
        return self.missions.get(mission_id)

    def list_by_journey(self, journey_id: str) -> List[Mission]:
        return [m for m in self.missions.values()]


@dataclass
class InMemoryEvidenceRepo:
    evidences: dict = field(default_factory=dict)

    def save(self, evidence: Evidence) -> None:
        self.evidences[evidence.id] = evidence

    def get(self, evidence_id: str) -> Optional[Evidence]:
        return self.evidences.get(evidence_id)

    def list_by_builder(self, builder_id: str) -> List[Evidence]:
        return [e for e in self.evidences.values() if e.builder_id == builder_id]


@dataclass
class InMemoryCompetencyRepo:
    competencies: dict = field(default_factory=dict)

    def save(self, competency: Competency) -> None:
        self.competencies[competency.id] = competency

    def get(self, competency_id: str) -> Optional[Competency]:
        return self.competencies.get(competency_id)

    def list_by_builder(self, builder_id: str) -> List[Competency]:
        return [c for c in self.competencies.values()]


@dataclass
class FakeEventBus:
    published: List[DomainEvent] = field(default_factory=list)

    def publish(self, events: List[DomainEvent]) -> None:
        self.published.extend(events)


class TestCreateBuilder:
    def test_success(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)

        result = service.create_builder(CreateBuilder(username="Alex"))

        assert isinstance(result, BuilderDTO)
        assert result.username == "Alex"
        assert result.level == 1
        assert result.xp == 0

    def test_persists_builder(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)

        service.create_builder(CreateBuilder(username="Maria"))

        assert len(repo.builders) == 1
        builder = list(repo.builders.values())[0]
        assert builder.username == "Maria"

    def test_publishes_event(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)

        service.create_builder(CreateBuilder(username="Joao"))

        assert len(bus.published) == 1
        assert bus.published[0].event_type.value == "builder_created"
        assert bus.published[0].payload["username"] == "Joao"


class TestGetBuilder:
    def test_success(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)
        builder = Builder("Ana")
        repo.save(builder)

        result = service.get_builder(builder.id)

        assert result.username == "Ana"

    def test_not_found(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)

        with pytest.raises(BuilderNotFound):
            service.get_builder("non-existent")


class TestGainXP:
    def test_success(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)
        builder = Builder("Carlos")
        repo.save(builder)

        result = service.gain_xp(builder.id, 500)

        assert result.xp == 500
        assert result.level == 2

    def test_not_found(self):
        repo = InMemoryBuilderRepo()
        bus = FakeEventBus()
        service = BuilderService(repo, bus)

        with pytest.raises(BuilderNotFound):
            service.gain_xp("invalid", 100)


class TestStartMission:
    def test_success(self):
        builder_repo = InMemoryBuilderRepo()
        mission_repo = InMemoryMissionRepo()
        evidence_repo = InMemoryEvidenceRepo()
        bus = FakeEventBus()
        service = MissionService(builder_repo, mission_repo, evidence_repo, bus)

        builder = Builder("Alex")
        builder_repo.save(builder)
        mission = Mission("Linux Explorer", "Navigate Linux")
        mission_repo.save(mission)

        result = service.start_mission(
            StartMission(builder_id=builder.id, mission_id=mission.id)
        )

        assert isinstance(result, MissionDTO)
        assert result.title == "Linux Explorer"
        assert result.status == "started"

    def test_builder_not_found(self):
        mission_repo = InMemoryMissionRepo()
        service = MissionService(
            InMemoryBuilderRepo(), mission_repo, InMemoryEvidenceRepo(), FakeEventBus()
        )
        mission = Mission("Test")
        mission_repo.save(mission)

        with pytest.raises(BuilderNotFound):
            service.start_mission(
                StartMission(builder_id="invalid", mission_id=mission.id)
            )

    def test_mission_not_found(self):
        builder_repo = InMemoryBuilderRepo()
        service = MissionService(
            builder_repo, InMemoryMissionRepo(), InMemoryEvidenceRepo(), FakeEventBus()
        )
        builder = Builder("Alex")
        builder_repo.save(builder)

        with pytest.raises(MissionNotFound):
            service.start_mission(
                StartMission(builder_id=builder.id, mission_id="invalid")
            )


class TestSubmitEvidence:
    def test_success(self):
        builder_repo = InMemoryBuilderRepo()
        mission_repo = InMemoryMissionRepo()
        evidence_repo = InMemoryEvidenceRepo()
        bus = FakeEventBus()
        service = MissionService(builder_repo, mission_repo, evidence_repo, bus)

        builder = Builder("Alex")
        builder_repo.save(builder)
        mission = Mission("Linux Explorer")
        mission_repo.save(mission)
        mission.start()

        result = service.submit_evidence(
            SubmitEvidence(
                builder_id=builder.id,
                mission_id=mission.id,
                artifact="terminal.log",
                evidence_type=EvidenceType.CODE,
            )
        )

        assert isinstance(result, EvidenceDTO)
        assert result.artifact == "terminal.log"
        assert result.status == "submitted"

    def test_publishes_events(self):
        builder_repo = InMemoryBuilderRepo()
        mission_repo = InMemoryMissionRepo()
        evidence_repo = InMemoryEvidenceRepo()
        bus = FakeEventBus()
        service = MissionService(builder_repo, mission_repo, evidence_repo, bus)

        builder = Builder("Alex")
        builder_repo.save(builder)
        mission = Mission("Linux Explorer")
        mission_repo.save(mission)
        mission.start()

        service.submit_evidence(
            SubmitEvidence(
                builder_id=builder.id,
                mission_id=mission.id,
                artifact="proof.md",
            )
        )

        assert len(bus.published) >= 1

    def test_builder_not_found(self):
        service = MissionService(
            InMemoryBuilderRepo(),
            InMemoryMissionRepo(),
            InMemoryEvidenceRepo(),
            FakeEventBus(),
        )

        with pytest.raises(BuilderNotFound):
            service.submit_evidence(
                SubmitEvidence(
                    builder_id="invalid",
                    mission_id="m1",
                    artifact="file.txt",
                )
            )


class TestUnlockCompetency:
    def test_success(self):
        builder_repo = InMemoryBuilderRepo()
        competency_repo = InMemoryCompetencyRepo()
        bus = FakeEventBus()
        service = CompetencyService(builder_repo, competency_repo, bus)

        builder = Builder("Alex")
        builder_repo.save(builder)

        result = service.unlock_competency(
            UnlockCompetency(
                builder_id=builder.id,
                name="Linux Administration",
                description="Administer Linux systems",
                level=1,
                criteria=["users", "permissions"],
            )
        )

        assert isinstance(result, BuilderDTO)
        assert result.competency_count == 1

    def test_persists_competency(self):
        builder_repo = InMemoryBuilderRepo()
        competency_repo = InMemoryCompetencyRepo()
        bus = FakeEventBus()
        service = CompetencyService(builder_repo, competency_repo, bus)

        builder = Builder("Alex")
        builder_repo.save(builder)

        service.unlock_competency(
            UnlockCompetency(builder_id=builder.id, name="Networking")
        )

        assert len(competency_repo.competencies) == 1

    def test_builder_not_found(self):
        service = CompetencyService(
            InMemoryBuilderRepo(), InMemoryCompetencyRepo(), FakeEventBus()
        )

        with pytest.raises(BuilderNotFound):
            service.unlock_competency(
                UnlockCompetency(builder_id="invalid", name="Test")
            )


class TestDTOImmutability:
    def test_builder_dto_attributes(self):
        dto = BuilderDTO(
            id="b1",
            username="Alex",
            level=3,
            xp=1200,
            competency_count=2,
            achievement_count=1,
            active_mission_count=1,
        )
        assert dto.id == "b1"
        assert dto.competency_count == 2

    def test_mission_dto_attributes(self):
        dto = MissionDTO(
            id="m1",
            title="Linux",
            objective="Learn Linux",
            difficulty=2,
            xp_reward=200,
            status="started",
        )
        assert dto.status == "started"


class TestServiceIntegration:
    def test_full_builder_lifecycle(self):
        builder_repo = InMemoryBuilderRepo()
        mission_repo = InMemoryMissionRepo()
        evidence_repo = InMemoryEvidenceRepo()
        competency_repo = InMemoryCompetencyRepo()
        bus = FakeEventBus()

        builder_svc = BuilderService(builder_repo, bus)
        mission_svc = MissionService(builder_repo, mission_repo, evidence_repo, bus)
        competency_svc = CompetencyService(builder_repo, competency_repo, bus)

        builder = builder_svc.create_builder(CreateBuilder(username="Alex"))
        assert builder.xp == 0

        mission = Mission("Docker Basics", "Learn containerization")
        mission_repo.save(mission)

        started = mission_svc.start_mission(
            StartMission(builder_id=builder.id, mission_id=mission.id)
        )
        assert started.status == "started"

        evidence = mission_svc.submit_evidence(
            SubmitEvidence(
                builder_id=builder.id,
                mission_id=mission.id,
                artifact="Dockerfile",
                evidence_type=EvidenceType.CODE,
            )
        )
        assert evidence.status == "submitted"

        builder_svc.gain_xp(builder.id, 200)
        updated = builder_svc.get_builder(builder.id)
        assert updated.xp == 200

        competency_svc.unlock_competency(
            UnlockCompetency(
                builder_id=builder.id,
                name="Docker",
                description="Container management",
            )
        )
        final = builder_svc.get_builder(builder.id)
        assert final.competency_count == 1
        assert len(bus.published) >= 4


class TestAssessmentService:
    def test_success_approval_transitions_to_accepted(self):
        evidence_repo = InMemoryEvidenceRepo()
        bus = FakeEventBus()
        service = AssessmentService(evidence_repo, bus)

        evidence = Evidence(artifact="my code", type=EvidenceType.CODE)
        evidence.submit("builder-1")
        evidence_repo.save(evidence)

        assessment = service.complete_assessment(
            CompleteAssessment(
                evidence_id=evidence.id,
                score=0.8,
                feedback="Excellent work",
                reviewer="Reviewer Agent",
            )
        )

        assert assessment.is_approved is True
        updated_evidence = evidence_repo.get(evidence.id)
        assert updated_evidence.status == EvidenceStatus.ACCEPTED

    def test_success_rejection_transitions_to_rejected(self):
        evidence_repo = InMemoryEvidenceRepo()
        bus = FakeEventBus()
        service = AssessmentService(evidence_repo, bus)

        evidence = Evidence(artifact="bad code", type=EvidenceType.CODE)
        evidence.submit("builder-1")
        evidence_repo.save(evidence)

        assessment = service.complete_assessment(
            CompleteAssessment(
                evidence_id=evidence.id,
                score=0.5,
                feedback="Needs improvement",
                reviewer="Reviewer Agent",
            )
        )

        assert assessment.is_approved is False
        updated_evidence = evidence_repo.get(evidence.id)
        assert updated_evidence.status == EvidenceStatus.REJECTED

    def test_policy_denies_already_accepted_evidence(self):
        evidence_repo = InMemoryEvidenceRepo()
        bus = FakeEventBus()
        service = AssessmentService(evidence_repo, bus)

        evidence = Evidence(artifact="my code", type=EvidenceType.CODE)
        evidence.submit("builder-1")
        evidence.accept()
        evidence_repo.save(evidence)

        with pytest.raises(EvidenceRequired) as exc:
            service.complete_assessment(
                CompleteAssessment(
                    evidence_id=evidence.id,
                    score=0.9,
                )
            )

        assert "Policy Violation [StateProtocol]" in str(exc.value)

    def test_policy_denies_missing_evidence(self):
        evidence_repo = InMemoryEvidenceRepo()
        bus = FakeEventBus()
        service = AssessmentService(evidence_repo, bus)

        with pytest.raises(EvidenceRequired) as exc:
            service.complete_assessment(
                CompleteAssessment(
                    evidence_id="invalid-id",
                    score=0.9,
                )
            )

        assert "Policy Violation [I2]" in str(exc.value)
