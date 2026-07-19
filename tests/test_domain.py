import pytest
from datetime import datetime

from src.ascend.domain import (
    Builder,
    Competency,
    Mission,
    Evidence,
    Assessment,
    Achievement,
    Skill,
    Journey,
    Challenge,
    DomainEvent,
    EventType,
    BuilderCreated,
    MissionStarted,
    EvidenceSubmitted,
    AssessmentCompleted,
    CompetencyUnlocked,
    AchievementEarned,
)
from src.ascend.domain.mission import MissionStatus
from src.ascend.domain.evidence import EvidenceStatus, EvidenceType


class TestBuilderCreation:
    def test_create_builder_with_username(self):
        builder = Builder("Alex")
        assert builder.username == "Alex"
        assert builder.level == 1
        assert builder.xp == 0
        assert builder.id == "builder-alex"

    def test_builder_creation_emits_event(self):
        builder = Builder("Maria")
        assert len(builder.events) == 1
        assert builder.events[0].event_type == EventType.BUILDER_CREATED
        assert builder.events[0].payload["username"] == "Maria"


class TestMissionLifecycle:
    def test_mission_starts_as_available(self):
        mission = Mission("Linux Explorer", "Navigate Linux filesystem")
        assert mission.status == MissionStatus.AVAILABLE
        assert not mission.is_active
        assert not mission.is_completed

    def test_mission_can_start(self):
        mission = Mission("Linux Explorer")
        mission.start()
        assert mission.status == MissionStatus.STARTED
        assert mission.is_active

    def test_mission_cannot_start_twice(self):
        mission = Mission("Linux Explorer")
        mission.start()
        with pytest.raises(ValueError, match="Cannot start mission"):
            mission.start()

    def test_mission_submit_evidence(self):
        mission = Mission("Linux Explorer")
        mission.start()
        evidence = Evidence("terminal.log", EvidenceType.DOCUMENT)
        mission.submit(evidence)
        assert mission.status == MissionStatus.EVIDENCE_SUBMITTED
        assert len(mission.evidence_list) == 1

    def test_mission_complete(self):
        mission = Mission("Linux Explorer")
        mission.start()
        evidence = Evidence("terminal.log")
        mission.submit(evidence)
        mission.complete()
        assert mission.is_completed

    def test_cannot_submit_before_start(self):
        mission = Mission("Linux Explorer")
        evidence = Evidence("log.txt")
        with pytest.raises(ValueError):
            mission.submit(evidence)

    def test_cannot_complete_without_submit(self):
        mission = Mission("Linux Explorer")
        with pytest.raises(ValueError):
            mission.complete()

    def test_mission_prerequisites(self):
        mission = Mission("Advanced Linux", prerequisites=["mission-linux-explorer"])
        assert not mission.can_start([])
        assert mission.can_start(["mission-linux-explorer"])


class TestEvidenceSubmission:
    def test_evidence_creation(self):
        evidence = Evidence("report.md")
        assert evidence.status == EvidenceStatus.SUBMITTED
        assert evidence.id.startswith("ev-")

    def test_evidence_submit(self):
        evidence = Evidence("project.tar.gz", EvidenceType.PROJECT)
        evidence.submit("builder-alex")
        assert evidence.status == EvidenceStatus.SUBMITTED
        assert evidence.builder_id == "builder-alex"
        assert evidence.submitted_at is not None

    def test_evidence_accept(self):
        evidence = Evidence("code.py")
        evidence.submit("builder-1")
        evidence.accept()
        assert evidence.status == EvidenceStatus.ACCEPTED

    def test_evidence_reject(self):
        evidence = Evidence("faulty.txt")
        evidence.submit("builder-1")
        evidence.reject()
        assert evidence.status == EvidenceStatus.REJECTED

    def test_builder_submits_evidence_for_mission(self):
        builder = Builder("Alex")
        mission = Mission("Linux Explorer")
        builder.start_mission(mission)
        evidence = Evidence("terminal.log")
        builder.submit_evidence(evidence, mission)
        assert mission.status == MissionStatus.EVIDENCE_SUBMITTED
        assert evidence in builder.evidence_list


class TestCompetencyProgression:
    def test_add_competency_to_builder(self):
        builder = Builder("Alex")
        competency = Competency("Linux Administration", "Administer Linux systems")
        builder.add_competency(competency)
        assert len(builder.competencies) == 1
        assert builder.competencies[0].name == "Linux Administration"

    def test_competency_level_upgrades(self):
        builder = Builder("Alex")
        c1 = Competency("Linux", level=1)
        c2 = Competency("Linux", level=3)
        builder.add_competency(c1)
        builder.add_competency(c2)
        assert builder.competencies[0].level == 3

    def test_xp_accumulation_and_level_up(self):
        builder = Builder("Alex")
        assert builder.level == 1
        builder.add_xp(500)
        assert builder.level == 2
        builder.add_xp(500)
        assert builder.level == 3
        assert builder.xp == 1000

    def test_xp_cannot_be_negative(self):
        builder = Builder("Alex")
        with pytest.raises(ValueError, match="XP cannot be negative"):
            builder.gain_xp(-10)

    def test_competency_increase_level(self):
        comp = Competency("Linux")
        comp.increase_level()
        assert comp.level == 2

    def test_competency_check_completion(self):
        comp = Competency("Linux", criteria=["users", "permissions", "processes"])
        assert comp.check_completion(["users", "permissions"])
        assert not comp.check_completion(["users"])


class TestAchievements:
    def test_achievement_creation(self):
        ach = Achievement(
            "Linux Builder",
            "Complete 10 Linux missions",
            criteria=["Complete 10 Linux missions"],
        )
        assert ach.id == "ach-linux-builder"
        assert not ach.is_earned

    def test_earn_achievement(self):
        ach = Achievement("First Mission")
        ach.earn()
        assert ach.is_earned
        assert ach.earned_at is not None

    def test_builder_can_earn_achievements(self):
        builder = Builder("Alex")
        ach = Achievement("First Mission")
        builder.add_achievement(ach)
        assert len(builder.achievements) == 1

    def test_no_duplicate_achievements(self):
        builder = Builder("Alex")
        ach = Achievement("First Mission")
        builder.add_achievement(ach)
        builder.add_achievement(ach)
        assert len(builder.achievements) == 1


class TestDomainEvents:
    def test_builder_created_event(self):
        event = BuilderCreated("builder-1", "Alex")
        assert event.event_type == EventType.BUILDER_CREATED
        assert event.aggregate_id == "builder-1"
        assert event.payload["username"] == "Alex"

    def test_mission_started_event(self):
        event = MissionStarted("mission-1", "builder-1")
        assert event.event_type == EventType.MISSION_STARTED

    def test_evidence_submitted_event(self):
        event = EvidenceSubmitted("ev-1", "mission-1", "builder-1")
        assert event.event_type == EventType.EVIDENCE_SUBMITTED

    def test_assessment_completed_event(self):
        event = AssessmentCompleted("assess-1", "ev-1", 0.85)
        assert event.event_type == EventType.ASSESSMENT_COMPLETED
        assert event.payload["score"] == 0.85

    def test_competency_unlocked_event(self):
        event = CompetencyUnlocked("comp-1", "builder-1", 2)
        assert event.event_type == EventType.COMPETENCY_UNLOCKED

    def test_achievement_earned_event(self):
        event = AchievementEarned("ach-1", "builder-1")
        assert event.event_type == EventType.ACHIEVEMENT_EARNED
        assert event.payload["achievement_id"] == "ach-1"

    def test_event_has_event_id(self):
        event = BuilderCreated("b-1", "Alex")
        assert event.event_id is not None
        assert event.event_id.startswith("evt-")

    def test_event_has_timestamp(self):
        event = BuilderCreated("b-1", "Alex")
        assert isinstance(event.timestamp, datetime)


class TestAssessment:
    def test_assessment_creation(self):
        assessment = Assessment("ev-1", 0.85, "Good work", "Reviewer Agent")
        assert assessment.id == "assess-ev-1"
        assert assessment.score == 0.85

    def test_assessment_approval_threshold(self):
        approved = Assessment("ev-1", 0.85)
        failed = Assessment("ev-2", 0.5)
        assert approved.is_approved
        assert not failed.is_approved

    def test_excellent_assessment(self):
        excellent = Assessment("ev-1", 0.95)
        assert excellent.is_excellent


class TestJourney:
    def test_journey_creation(self):
        journey = Journey("Cyber Security", "Master security fundamentals")
        assert journey.id == "journey-cyber-security"
        assert journey.status.value == "available"

    def test_journey_with_missions(self):
        m1 = Mission("Linux Basics")
        m2 = Mission("Network Security")
        journey = Journey("Cyber Security", missions=[m1, m2])
        assert len(journey.missions) == 2


class TestSkill:
    def test_skill_creation(self):
        skill = Skill("File Permissions", "Understanding Linux file permissions", 0.5)
        assert skill.id == "skill-file-permissions"
        assert skill.weight == 0.5


class TestChallenge:
    def test_challenge_creation(self):
        challenge = Challenge(
            "Configure SSH securely",
            requirements=["Disable root login", "Use key-based auth"],
        )
        assert challenge.id.startswith("challenge-")
        assert len(challenge.requirements) == 2


class TestBuilderMissionFlow:
    def test_full_builder_mission_flow(self):
        builder = Builder("Alex")
        assert builder.level == 1

        mission = Mission("Linux Explorer", "Navigate Linux", xp_reward=100)
        builder.start_mission(mission)
        assert mission.is_active

        evidence = Evidence("terminal.log", EvidenceType.CODE)
        builder.submit_evidence(evidence, mission)
        assert evidence.status == EvidenceStatus.SUBMITTED

        mission.complete()
        builder.add_xp(mission.xp_reward)
        assert mission.is_completed
        assert builder.xp == 100

        competency = Competency("Linux Administration", level=1)
        builder.add_competency(competency)
        assert len(builder.competencies) == 1

    def test_builder_active_missions(self):
        builder = Builder("Alex")
        m1 = Mission("Mission 1")
        m2 = Mission("Mission 2")
        builder.start_mission(m1)
        builder.start_mission(m2)
        assert len(builder.active_missions) == 2
        assert len(builder.completed_missions) == 0
