import pytest
from datetime import datetime, timedelta
from pathlib import Path

from ascend.domain.builder import Builder
from ascend.package_engine.models import (
    AchievementDef as APSAchievement,
    CompetencyDef as APSCompetency,
    Journey as APSJourney,
    Mission as APSMission,
    Package as APSPackage,
    Rubric as APSRubric,
    RubricCriterion as APSRubricCriterion,
)
from ascend.shared.clock import Clock

from ascend.runtime.adapters.package_converter import PackageConverter
from ascend.runtime.assessment.pipeline import AssessmentPipeline
from ascend.runtime.competency.engine import CompetencyEngine
from ascend.runtime.context import RuntimeContext
from ascend.runtime.events.collector import DomainEventCollector
from ascend.runtime.hooks import NoopHooks, RuntimeHooks
from ascend.runtime.kernel import RuntimeKernel
from ascend.runtime.models import (
    RuntimeAchievement,
    RuntimeChallenge,
    RuntimeCompetency,
    RuntimeCriterion,
    RuntimeJourney,
    RuntimeMission,
    RuntimePackage,
    RuntimeRubric,
)
from ascend.runtime.orchestrator import RuntimeOrchestrator
from ascend.runtime.report import AssessmentResult, CompetencyUpdate, ExecutionReport
from ascend.runtime.runners.challenge_runner import ChallengeRunner
from ascend.runtime.runners.journey_runner import JourneyRunner
from ascend.runtime.runners.mission_runner import MissionRunner


PACKAGES_DIR = Path(__file__).resolve().parent.parent / "packages"


@pytest.fixture
def clock():
    class FakeClock(Clock):
        def __init__(self):
            self._now = datetime(2026, 1, 1)

        def now(self) -> datetime:
            return self._now

        def advance(self, seconds: int = 1):
            self._now += timedelta(seconds=seconds)

    return FakeClock()


@pytest.fixture
def collector():
    return DomainEventCollector()


@pytest.fixture
def assessment():
    return AssessmentPipeline()


@pytest.fixture
def competency_engine():
    return CompetencyEngine()


@pytest.fixture
def challenge_runner():
    return ChallengeRunner()


@pytest.fixture
def hooks():
    return NoopHooks()


@pytest.fixture
def builder():
    return Builder("test-user")


@pytest.fixture
def sample_rubric():
    return RuntimeRubric(
        id="test-rubric",
        title="Teste",
        criteria={
            "a": RuntimeCriterion(weight=50, description="Qualidade do código"),
            "b": RuntimeCriterion(weight=50, description="Organização"),
        },
    )


@pytest.fixture
def sample_mission():
    return RuntimeMission(
        id="m1",
        title="Missão 1",
        description="Primeira missão",
        difficulty="beginner",
        estimated_minutes=60,
        xp=100,
        prerequisites=[],
        competencies=["comp-1"],
        challenge=RuntimeChallenge(
            type="practical",
            description="Crie um script",
            evidence_required=True,
            evidence_types=["code"],
        ),
        rubric_id="test-rubric",
    )


@pytest.fixture
def sample_journey(sample_mission):
    return RuntimeJourney(
        id="j1",
        title="Jornada 1",
        description="Teste",
        difficulty="beginner",
        estimated_hours=10,
        missions=[sample_mission],
        unlocks=[],
    )


@pytest.fixture
def sample_package(sample_journey):
    return RuntimePackage(
        id="test-pkg",
        version="1.0.0",
        title="Teste",
        description="Pacote de teste",
        author="Tester",
        journeys=[sample_journey],
        competencies={
            "comp-1": RuntimeCompetency(
                id="comp-1",
                name="Comp 1",
                description="Competência 1",
                level="beginner",
                evidence_required=True,
                mastery_threshold=50,
            ),
        },
        rubrics={
            "test-rubric": RuntimeRubric(
                id="test-rubric",
                title="Teste",
                criteria={
                    "a": RuntimeCriterion(weight=50, description="Qualidade do código"),
                    "b": RuntimeCriterion(weight=50, description="Organização"),
                },
            ),
        },
        achievements={
            "ach-1": RuntimeAchievement(
                id="ach-1",
                name="Primeira Conquista",
                description="Completou a primeira missão",
                criteria=["completar comp-1"],
                badge="badge-1",
            ),
        },
        dependencies=[],
        capabilities=["evidence"],
    )


class TestDomainEventCollector:
    def test_collect_and_drain(self, collector):
        collector.collect("event1")
        collector.collect("event2")
        assert len(collector.collected()) == 2
        drained = collector.drain()
        assert len(drained) == 2
        assert len(collector.collected()) == 0

    def test_clear(self, collector):
        collector.collect("event1")
        collector.clear()
        assert len(collector.collected()) == 0


class TestRuntimeHooks:
    def test_noop_hooks_do_nothing(self, hooks):
        hooks.before_journey("j1", None)
        hooks.after_journey("j1", None)
        hooks.before_mission("m1", None)
        hooks.after_mission("m1", None)
        hooks.before_assessment("m1", None)
        hooks.after_assessment("m1", None)


class TestAssessmentPipeline:
    def test_assessment_with_rubric(self, assessment, sample_rubric):
        result = assessment.run(
            evidence_text="código organizado e de qualidade",
            rubric=sample_rubric,
            mission_id="m1",
        )
        assert result.passed is True
        assert result.rubric_id == "test-rubric"
        assert result.total_score > 0

    def test_assessment_empty_evidence_fails(self, assessment, sample_rubric):
        result = assessment.run(
            evidence_text="",
            rubric=sample_rubric,
            mission_id="m1",
        )
        assert result.passed is False
        assert result.percentage == 0.0

    def test_assessment_without_rubric_simple_pass(self, assessment):
        result = assessment.run(
            evidence_text="some evidence",
            rubric=None,
            mission_id="m1",
        )
        assert result.passed is True
        assert result.percentage == 100.0

    def test_assessment_rubric_scores(self, assessment):
        rubric = RuntimeRubric(
            id="r1",
            title="R1",
            criteria={
                "x": RuntimeCriterion(weight=40, description="teste xyz abc"),
                "y": RuntimeCriterion(weight=60, description="outro criterio"),
            },
        )
        result = assessment.run(
            evidence_text="teste xyz abc",
            rubric=rubric,
            mission_id="m1",
        )
        assert result.max_score == 100
        assert result.scores["x"] >= 10


class TestCompetencyEngine:
    def test_process_passed_mission(self, competency_engine, sample_mission, sample_package):
        result = AssessmentResult(
            mission_id="m1",
            rubric_id="test-rubric",
            scores={"a": 40, "b": 40},
            total_score=80,
            max_score=100,
            percentage=80.0,
            passed=True,
            evidence_text="code",
        )
        update = competency_engine.process(
            result=result,
            mission=sample_mission,
            package=sample_package,
            current_xp=0,
            current_level=1,
            unlocked_competency_ids=set(),
            earned_achievement_ids=set(),
        )
        assert update.xp_gained == 100
        assert update.new_xp == 100
        assert update.new_level == 1
        assert update.unlocked is True

    def test_process_failed_mission_no_xp(self, competency_engine, sample_mission, sample_package):
        result = AssessmentResult(
            mission_id="m1",
            rubric_id="test-rubric",
            scores={"a": 10, "b": 10},
            total_score=20,
            max_score=100,
            percentage=20.0,
            passed=False,
            evidence_text="bad",
        )
        update = competency_engine.process(
            result=result,
            mission=sample_mission,
            package=sample_package,
            current_xp=0,
            current_level=1,
            unlocked_competency_ids=set(),
            earned_achievement_ids=set(),
        )
        assert update.xp_gained == 0
        assert update.new_xp == 0
        assert update.unlocked is False

    def test_level_up_at_500_xp(self, competency_engine, sample_mission, sample_package):
        result = AssessmentResult(
            mission_id="m1",
            rubric_id="test-rubric",
            scores={"a": 50, "b": 50},
            total_score=100,
            max_score=100,
            percentage=100.0,
            passed=True,
            evidence_text="code",
        )
        update = competency_engine.process(
            result=result,
            mission=sample_mission,
            package=sample_package,
            current_xp=450,
            current_level=1,
            unlocked_competency_ids=set(),
            earned_achievement_ids=set(),
        )
        assert update.xp_gained == 100
        assert update.new_xp == 550
        assert update.new_level == 2

    def test_achievement_unlocked(self, competency_engine, sample_mission, sample_package):
        result = AssessmentResult(
            mission_id="m1",
            rubric_id="test-rubric",
            scores={"a": 50, "b": 50},
            total_score=100,
            max_score=100,
            percentage=100.0,
            passed=True,
            evidence_text="code",
        )
        update = competency_engine.process(
            result=result,
            mission=sample_mission,
            package=sample_package,
            current_xp=0,
            current_level=1,
            unlocked_competency_ids=set(),
            earned_achievement_ids=set(),
        )
        assert len(update.achievements_unlocked) > 0
        assert "ach-1" in update.achievements_unlocked


class TestChallengeRunner:
    def test_open_returns_description(self, challenge_runner, sample_mission):
        desc = challenge_runner.open(sample_mission, None)
        assert desc == "Crie um script"

    def test_collect_evidence_from_context(self, challenge_runner, sample_mission, builder, collector, clock):
        ctx = RuntimeContext(
            builder=builder,
            package=RuntimePackage(
                id="t", version="1", title="", description="", author="",
                journeys=[], competencies={}, rubrics={}, achievements={},
                dependencies=[], capabilities=[],
            ),
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
            evidence_input={"m1": "meu código"},
        )
        evidence = challenge_runner.collect_evidence(sample_mission, ctx)
        assert evidence == "meu código"

    def test_collect_evidence_empty_when_missing(self, challenge_runner, sample_mission, builder, collector, clock):
        ctx = RuntimeContext(
            builder=builder,
            package=RuntimePackage(
                id="t", version="1", title="", description="", author="",
                journeys=[], competencies={}, rubrics={}, achievements={},
                dependencies=[], capabilities=[],
            ),
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
        )
        evidence = challenge_runner.collect_evidence(sample_mission, ctx)
        assert evidence == ""


class TestMissionRunner:
    def test_run_completes_mission_with_evidence(
        self, assessment, competency_engine, challenge_runner, builder, collector, clock, sample_mission, sample_package
    ):
        runner = MissionRunner(assessment, competency_engine, challenge_runner)
        ctx = RuntimeContext(
            builder=builder,
            package=sample_package,
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
            evidence_input={"m1": "código organizado e de qualidade com boa estrutura"},
        )
        result = runner.run(sample_mission, builder, ctx)
        assert result.started is True
        assert result.completed is True
        assert result.evidence_submitted is True
        assert result.assessment_result is not None
        assert result.assessment_result.passed is True

    def test_run_without_evidence_no_xp(
        self, assessment, competency_engine, challenge_runner, builder, collector, clock, sample_mission, sample_package
    ):
        runner = MissionRunner(assessment, competency_engine, challenge_runner)
        ctx = RuntimeContext(
            builder=builder,
            package=sample_package,
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
        )
        result = runner.run(sample_mission, builder, ctx)
        assert result.started is True
        assert result.completed is False
        assert result.evidence_submitted is False

    def test_events_collected_during_run(
        self, assessment, competency_engine, challenge_runner, builder, collector, clock, sample_mission, sample_package
    ):
        runner = MissionRunner(assessment, competency_engine, challenge_runner)
        ctx = RuntimeContext(
            builder=builder,
            package=sample_package,
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
            evidence_input={"m1": "código organizado e de qualidade"},
        )
        runner.run(sample_mission, builder, ctx)
        events = collector.drain()
        event_types = {e.event_type.value for e in events if hasattr(e, 'event_type')}
        assert "mission_started" in event_types
        assert "evidence_submitted" in event_types
        assert "assessment_completed" in event_types


class TestJourneyRunner:
    def test_run_journey_completes_all_missions(
        self, assessment, competency_engine, challenge_runner, builder, collector, clock, sample_mission
    ):
        mission_runner = MissionRunner(assessment, competency_engine, challenge_runner)
        journey_runner = JourneyRunner(mission_runner)
        journey = RuntimeJourney(
            id="j1",
            title="J1",
            description="",
            difficulty="beginner",
            estimated_hours=10,
            missions=[sample_mission],
            unlocks=[],
        )
        package = RuntimePackage(
            id="t", version="1", title="", description="", author="",
            journeys=[journey],
            competencies={
                "comp-1": RuntimeCompetency(
                    id="comp-1", name="Comp 1", description="",
                    level="beginner", evidence_required=True, mastery_threshold=50,
                ),
            },
            rubrics={
                "test-rubric": RuntimeRubric(
                    id="test-rubric", title="T",
                    criteria={"a": RuntimeCriterion(weight=100, description="teste qualidade")},
                ),
            },
            achievements={},
            dependencies=[], capabilities=["evidence"],
        )
        ctx = RuntimeContext(
            builder=builder,
            package=package,
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
            evidence_input={"m1": "código de qualidade"},
        )
        result = journey_runner.run(journey, builder, ctx)
        assert result.started is True
        assert result.completed is True
        assert len(result.mission_results) == 1
        assert result.mission_results[0].completed is True


class TestRuntimeOrchestrator:
    def test_orchestrator_full_flow(self, builder, collector, clock, sample_package):
        orchestrator = RuntimeOrchestrator()
        ctx = RuntimeContext(
            builder=builder,
            package=sample_package,
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
            evidence_input={"m1": "código organizado e de qualidade com boa estrutura"},
        )
        report = orchestrator.run(ctx)
        assert report.success is True
        assert report.journeys_completed >= 0
        assert report.missions_completed >= 0

    def test_orchestrator_handles_errors_gracefully(
        self, builder, collector, clock, sample_mission
    ):
        broken_package = RuntimePackage(
            id="broken", version="1", title="", description="", author="",
            journeys=[], competencies={}, rubrics={}, achievements={},
            dependencies=[], capabilities=[],
        )
        orchestrator = RuntimeOrchestrator()
        ctx = RuntimeContext(
            builder=builder,
            package=broken_package,
            clock=clock,
            event_collector=collector,
            hooks=NoopHooks(),
        )
        report = orchestrator.run(ctx)
        assert report.success is True


class TestPackageConverter:
    def test_convert_full_package(self):
        aps_pkg = APSPackage(
            id="conv-test",
            version="2.0.0",
            title="Convertido",
            description="Teste de conversão",
            author="Dev",
            journeys=[
                APSJourney(
                    id="j1",
                    title="J1",
                    description="",
                    missions=[
                        APSMission(
                            id="m1",
                            title="M1",
                            difficulty="beginner",
                            estimated_minutes=30,
                            xp=50,
                            prerequisites=[],
                            competencies=["c1"],
                            challenge_type="quiz",
                            challenge_description="Responda",
                            evidence_required=True,
                            evidence_types=["code"],
                            rubric="r1",
                        ),
                    ],
                ),
            ],
            competencies=[
                APSCompetency(id="c1", name="C1", level="beginner"),
            ],
            rubrics=[
                APSRubric(
                    id="r1", title="R1",
                    criteria={
                        "x": APSRubricCriterion(weight=100, description="critério"),
                    },
                ),
            ],
            achievements=[
                APSAchievement(id="a1", name="A1", criteria=["teste"], badge="b1"),
            ],
        )
        converter = PackageConverter()
        runtime_pkg = converter.convert(aps_pkg)
        assert runtime_pkg.id == "conv-test"
        assert len(runtime_pkg.journeys) == 1
        assert runtime_pkg.journeys[0].id == "j1"
        assert len(runtime_pkg.journeys[0].missions) == 1
        assert runtime_pkg.journeys[0].missions[0].id == "m1"
        assert "c1" in runtime_pkg.competencies
        assert "r1" in runtime_pkg.rubrics
        assert "a1" in runtime_pkg.achievements

    def test_convert_empty_package(self):
        aps_pkg = APSPackage(id="empty", version="1.0")
        converter = PackageConverter()
        runtime_pkg = converter.convert(aps_pkg)
        assert runtime_pkg.journeys == []
        assert runtime_pkg.competencies == {}
        assert runtime_pkg.rubrics == {}
        assert runtime_pkg.achievements == {}


class TestRuntimeKernel:
    def test_kernel_runs_cyber_foundations(self, clock, builder):
        kernel = RuntimeKernel(clock=clock)
        report = kernel.run(
            package_path=PACKAGES_DIR / "cyber-foundations",
            builder=builder,
            evidence_input={
                "html-foundations": "<html><header>Cabeçalho</header><main>Conteúdo</main><footer>Rodapé</footer></html>",
            },
        )
        assert report.success is True
        assert report.missions_completed >= 1

    def test_kernel_returns_report_with_xp(self, clock, builder):
        kernel = RuntimeKernel(clock=clock)
        report = kernel.run(
            package_path=PACKAGES_DIR / "cyber-foundations",
            builder=builder,
            evidence_input={
                "html-foundations": "<html><header>Cabeçalho</header><main>Conteúdo</main><footer>Rodapé</footer></html>",
            },
        )
        assert isinstance(report, ExecutionReport)
        assert report.package_id == "cyber-foundations"
        assert report.builder_username == "test-user"

    def test_kernel_validates_package_before_run(self, clock, tmp_path):
        kernel = RuntimeKernel(clock=clock)
        invalid_dir = tmp_path / "invalid"
        invalid_dir.mkdir()
        (invalid_dir / "package.yaml").write_text(
            "metadata:\n  id: ''\n  version: ''\n", encoding="utf-8"
        )
        builder = Builder("tester")
        report = kernel.run(
            package_path=invalid_dir,
            builder=builder,
        )
        assert report.success is False
        assert len(report.errors) > 0

    def test_kernel_without_evidence_still_runs(self, clock, builder):
        kernel = RuntimeKernel(clock=clock)
        report = kernel.run(
            package_path=PACKAGES_DIR / "cyber-foundations",
            builder=builder,
        )
        assert report.success is True

    def test_hooks_are_called(self, clock, builder):
        class TrackingHooks(NoopHooks):
            def __init__(self):
                self.calls = []

            def _track(self, name, *args):
                self.calls.append(name)

            def before_journey(self, journey_id, context):
                self._track("before_journey")

            def after_journey(self, journey_id, context):
                self._track("after_journey")

            def before_mission(self, mission_id, context):
                self._track("before_mission")

            def after_mission(self, mission_id, context):
                self._track("after_mission")

            def before_assessment(self, mission_id, context):
                self._track("before_assessment")

            def after_assessment(self, mission_id, context):
                self._track("after_assessment")

        hooks = TrackingHooks()
        kernel = RuntimeKernel(clock=clock, hooks=hooks)
        kernel.run(
            package_path=PACKAGES_DIR / "cyber-foundations",
            builder=builder,
            evidence_input={
                "html-foundations": "<html><header>C</header><main>M</main><footer>F</footer></html>",
            },
        )
        assert "before_journey" in hooks.calls
        assert "after_journey" in hooks.calls
        assert "before_mission" in hooks.calls

    def test_report_structure(self, clock, builder):
        kernel = RuntimeKernel(clock=clock)
        report = kernel.run(
            package_path=PACKAGES_DIR / "cyber-foundations",
            builder=builder,
            evidence_input={
                "html-foundations": "código semântico e organizado com header main footer qualidade",
            },
        )
        assert hasattr(report, "success")
        assert hasattr(report, "missions_completed")
        assert hasattr(report, "total_xp")
        assert hasattr(report, "competencies_unlocked")
        assert hasattr(report, "achievements_earned")
        assert hasattr(report, "duration")
        assert report.duration >= 0
