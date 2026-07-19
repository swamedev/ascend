import pytest
from pathlib import Path

from ascend import Runtime
from ascend.domain.builder import Builder
from ascend.runtime.report import ExecutionReport

PACKAGES_DIR = Path(__file__).resolve().parent.parent / "packages"


class TestRuntimeAPI:
    def test_run_with_path_and_builder_name(self):
        rt = Runtime()
        report = rt.run(
            package=PACKAGES_DIR / "cyber-foundations",
            builder="alice",
            evidence={"html-foundations": "<html><body>test</body></html>"},
        )
        assert isinstance(report, ExecutionReport)
        assert report.builder_username == "alice"
        assert report.success is True

    def test_run_with_builder_object(self):
        rt = Runtime()
        builder = Builder("bob")
        report = rt.run(
            package=PACKAGES_DIR / "cyber-foundations",
            builder=builder,
            evidence={"html-foundations": "código HTML semântico organizado e de qualidade com tags"},
        )
        assert report.success is True
        assert report.builder_username == "bob"

    def test_run_with_string_evidence(self):
        rt = Runtime()
        report = rt.run(
            package=PACKAGES_DIR / "cyber-foundations",
            builder="carol",
            evidence="código HTML semântico com header main footer e organização",
        )
        assert report.success is True

    def test_report_has_summary(self):
        rt = Runtime()
        report = rt.run(
            package=PACKAGES_DIR / "cyber-foundations",
            builder="dave",
            evidence={"html-foundations": "código HTML semântico organizado e de qualidade com boa estrutura"},
        )
        summary = report.summary()
        assert isinstance(summary, str)
        assert "Journey:" in summary
        assert "Mission:" in summary

    def test_run_invalid_package_returns_error_report(self):
        rt = Runtime()
        report = rt.run(
            package=Path(".") / "nonexistent",
            builder="test",
        )
        assert report.success is False


class TestReportSummary:
    def test_summary_shows_success(self):
        report = ExecutionReport(
            success=True,
            package_id="p1",
            builder_username="u",
            duration=1.0,
            journeys_completed=1,
            missions_completed=1,
            total_xp=150,
            competencies_unlocked=[],
            achievements_earned=[],
            journey_results=[],
        )
        s = report.summary()
        assert "Journey completed successfully." in s

    def test_summary_shows_errors(self):
        report = ExecutionReport(
            success=False,
            package_id="p1",
            builder_username="u",
            duration=1.0,
            journeys_completed=0,
            missions_completed=0,
            total_xp=0,
            competencies_unlocked=[],
            achievements_earned=[],
            errors=["Package not found"],
        )
        s = report.summary()
        assert "Error: Package not found" in s

    def test_summary_shows_journey_results(self):
        from ascend.runtime.report import JourneyResult, MissionResult, CompetencyUpdate

        report = ExecutionReport(
            success=True,
            package_id="p1",
            builder_username="u",
            duration=1.0,
            journeys_completed=1,
            missions_completed=1,
            total_xp=100,
            competencies_unlocked=["c1"],
            achievements_earned=[],
            journey_results=[
                JourneyResult(
                    journey_id="j1",
                    started=True,
                    completed=True,
                    mission_results=[
                        MissionResult(
                            mission_id="m1",
                            started=True,
                            completed=True,
                            evidence_submitted=True,
                            competency_updates=[
                                CompetencyUpdate(
                                    competency_id="c1",
                                    unlocked=True,
                                    xp_gained=100,
                                    previous_xp=0,
                                    new_xp=100,
                                    previous_level=1,
                                    new_level=1,
                                    achievements_unlocked=[],
                                )
                            ],
                        )
                    ],
                )
            ],
        )
        s = report.summary()
        assert "[OK] Journey: j1" in s
        assert "[OK] Mission: m1" in s
        assert "XP +100" in s
        assert "Competency unlocked: c1" in s


class TestCLI:
    def test_cli_version(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "ascend.cli.main", "--version"],
            capture_output=True, text=True,
        )
        assert result.returncode == 0
        assert "ASCEND Runtime" in result.stdout

    def test_cli_validate_valid_package(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "ascend.cli.main", "package", "validate",
             str(PACKAGES_DIR / "cyber-foundations")],
            capture_output=True, text=True,
        )
        assert "is valid" in result.stdout

    def test_cli_validate_invalid_package(self, tmp_path):
        import subprocess, sys
        pkg_dir = tmp_path / "bad"
        pkg_dir.mkdir()
        (pkg_dir / "package.yaml").write_text(
            "metadata:\n  id: ''\n  version: ''\n", encoding="utf-8"
        )
        result = subprocess.run(
            [sys.executable, "-m", "ascend.cli.main", "package", "validate",
             str(pkg_dir)],
            capture_output=True, text=True,
        )
        assert result.returncode != 0
        assert "failed" in result.stdout

    def test_cli_run_basic(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "ascend.cli.main", "run",
             str(PACKAGES_DIR / "cyber-foundations"),
             "--builder", "cli-test",
             "--evidence", "código HTML semântico organizado e de qualidade com boa estrutura"],
            capture_output=True, text=True,
        )
        assert "Journey completed" in result.stdout

    def test_cli_init_creates_package(self, tmp_path):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, "-m", "ascend.cli.main", "init", "test-pkg"],
            capture_output=True, text=True, cwd=str(tmp_path),
        )
        assert result.returncode == 0
        assert (tmp_path / "test-pkg" / "package.yaml").exists()
