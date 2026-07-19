from pathlib import Path

from .models import Package
from .parser import PackageParser
from .validator import PackageValidator, ValidationResult


class PackageLoader:
    def __init__(self) -> None:
        self._parser = PackageParser()
        self._validator = PackageValidator()

    def load(self, package_path: str | Path) -> tuple[Package, ValidationResult]:
        path = Path(package_path)
        pkg = self._parse(path)
        result = self._validator.validate(pkg)
        return pkg, result

    def load_and_validate(self, package_path: str | Path) -> Package:
        pkg, result = self.load(package_path)
        if not result.valid:
            msgs = [f"  [{e.level}] {e.rule}: {e.message}" for e in result.errors]
            raise ValueError(
                f"Package validation failed:\n" + "\n".join(msgs)
            )
        return pkg

    def _parse(self, path: Path) -> Package:
        pkg_yaml = path / "package.yaml"
        pkg = self._parser.parse_package(self._parser.load_yaml(pkg_yaml))

        comp_path = path / "competencies" / "competencies.yaml"
        if comp_path.exists():
            pkg.competencies = self._parser.parse_competencies(
                self._parser.load_yaml(comp_path)
            )

        ach_path = path / "achievements" / "achievements.yaml"
        if ach_path.exists():
            pkg.achievements = self._parser.parse_achievements(
                self._parser.load_yaml(ach_path)
            )

        rubrics_path = path / "assessments" / "rubrics.yaml"
        if rubrics_path.exists():
            pkg.rubrics = self._parser.parse_rubrics(
                self._parser.load_yaml(rubrics_path)
            )

        journeys_dir = path / "journeys"
        if journeys_dir.exists():
            for journey_dir in sorted(journeys_dir.iterdir()):
                if journey_dir.is_dir():
                    journey = self._load_journey(journey_dir)
                    if journey:
                        pkg.journeys.append(journey)

        return pkg

    def _load_journey(self, journey_dir: Path) -> object | None:
        journey_yaml = journey_dir / "journey.yaml"
        if not journey_yaml.exists():
            return None
        journey = self._parser.parse_journey(self._parser.load_yaml(journey_yaml))

        missions_dir = journey_dir / "missions"
        if missions_dir.exists():
            for mission_dir in sorted(missions_dir.iterdir()):
                if mission_dir.is_dir():
                    mission = self._load_mission(mission_dir)
                    if mission:
                        journey.missions.append(mission)
        return journey

    def _load_mission(self, mission_dir: Path) -> object | None:
        mission_yaml = mission_dir / "mission.yaml"
        if not mission_yaml.exists():
            return None
        return self._parser.parse_mission(self._parser.load_yaml(mission_yaml))
