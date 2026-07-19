import pytest
import yaml
from pathlib import Path

from ascend.package_engine import (
    Package,
    Journey,
    Mission,
    CompetencyDef,
    AchievementDef,
    Rubric,
    RubricCriterion,
    PackageParser,
    PackageValidator,
    ValidationResult,
    ValidationIssue,
    PackageLoader,
)

PACKAGES_DIR = Path(__file__).resolve().parent.parent / "packages"


@pytest.fixture
def parser():
    return PackageParser()


@pytest.fixture
def validator():
    return PackageValidator()


@pytest.fixture
def loader():
    return PackageLoader()


@pytest.fixture
def cyber_pkg(loader):
    pkg, _ = loader.load(PACKAGES_DIR / "cyber-foundations")
    return pkg


class TestParser:
    def test_parse_package(self, parser):
        data = {
            "metadata": {
                "id": "test-pkg",
                "version": "1.0.0",
                "title": "Test",
                "author": "Tester",
                "license": "MIT",
            },
            "spec": {
                "runtime": ">=1.0",
                "language": "en",
                "dependencies": ["base-core"],
            },
            "capabilities": ["evidence", "plugin"],
        }
        pkg = parser.parse_package(data)
        assert pkg.id == "test-pkg"
        assert pkg.version == "1.0.0"
        assert pkg.author == "Tester"
        assert pkg.dependencies == ["base-core"]
        assert pkg.capabilities == ["evidence", "plugin"]

    def test_parse_journey(self, parser):
        data = {
            "metadata": {"id": "web-fundamentals", "title": "Web"},
            "spec": {"difficulty": "intermediate", "estimated_hours": 15, "unlocks": ["advanced"]},
        }
        j = parser.parse_journey(data)
        assert j.id == "web-fundamentals"
        assert j.difficulty == "intermediate"
        assert j.unlocks == ["advanced"]

    def test_parse_mission(self, parser):
        data = {
            "metadata": {"id": "html-basics", "title": "HTML Basics"},
            "spec": {
                "difficulty": "beginner",
                "estimated_minutes": 90,
                "xp": 100,
                "prerequisites": [],
                "competencies": ["html-fundamental"],
                "challenge": {"type": "practical", "description": "Build a page"},
                "evidence": {"required": True, "types": ["code"]},
                "assessment": {"rubric": "html-quality"},
            },
        }
        m = parser.parse_mission(data)
        assert m.id == "html-basics"
        assert m.xp == 100
        assert m.competencies == ["html-fundamental"]
        assert m.challenge_type == "practical"
        assert m.rubric == "html-quality"

    def test_parse_competencies(self, parser):
        data = {
            "spec": {
                "competencies": [
                    {"id": "c1", "name": "Comp 1", "level": "beginner", "mastery_threshold": 80},
                    {"id": "c2", "name": "Comp 2", "level": "advanced", "mastery_threshold": 90},
                ]
            }
        }
        comps = parser.parse_competencies(data)
        assert len(comps) == 2
        assert comps[0].id == "c1"
        assert comps[1].level == "advanced"

    def test_parse_achievements(self, parser):
        data = {
            "spec": {
                "achievements": [
                    {"id": "a1", "name": "First", "criteria": ["Do X"], "badge": "b1"},
                ]
            }
        }
        achs = parser.parse_achievements(data)
        assert len(achs) == 1
        assert achs[0].id == "a1"
        assert achs[0].badge == "b1"

    def test_parse_rubrics(self, parser):
        data = {
            "spec": {
                "rubrics": [
                    {
                        "id": "r1",
                        "title": "Quality",
                        "criteria": {
                            "a": {"weight": 40, "description": "Criterion A"},
                            "b": {"weight": 60, "description": "Criterion B"},
                        },
                    }
                ]
            }
        }
        rubrics = parser.parse_rubrics(data)
        assert len(rubrics) == 1
        assert rubrics[0].id == "r1"
        assert rubrics[0].criteria["a"].weight == 40
        assert rubrics[0].criteria["b"].weight == 60


class TestCyberPackage:
    def test_loads_successfully(self, cyber_pkg):
        assert cyber_pkg.id == "cyber-foundations"
        assert cyber_pkg.version == "1.0.0"
        assert cyber_pkg.title == "Cyber Foundations"
        assert cyber_pkg.language == "pt-BR"

    def test_has_competencies(self, cyber_pkg):
        assert len(cyber_pkg.competencies) == 3
        ids = {c.id for c in cyber_pkg.competencies}
        assert ids == {"html-fundamental", "css-fundamental", "logica-programacao"}

    def test_has_achievements(self, cyber_pkg):
        assert len(cyber_pkg.achievements) == 2
        ids = {a.id for a in cyber_pkg.achievements}
        assert ids == {"primeiro-site", "logica-zero"}

    def test_has_rubrics(self, cyber_pkg):
        assert len(cyber_pkg.rubrics) == 2
        ids = {r.id for r in cyber_pkg.rubrics}
        assert ids == {"html-quality", "css-quality"}

    def test_has_two_journeys(self, cyber_pkg):
        assert len(cyber_pkg.journeys) == 2
        jids = {j.id for j in cyber_pkg.journeys}
        assert jids == {"fundamentos-web", "logica-programacao"}

    def test_fundamentos_web_has_missions(self, cyber_pkg):
        web = next(j for j in cyber_pkg.journeys if j.id == "fundamentos-web")
        assert len(web.missions) == 2
        mids = {m.id for m in web.missions}
        assert mids == {"html-foundations", "css-foundations"}

    def test_mission_references_competencies(self, cyber_pkg):
        web = next(j for j in cyber_pkg.journeys if j.id == "fundamentos-web")
        html = next(m for m in web.missions if m.id == "html-foundations")
        assert html.competencies == ["html-fundamental"]
        assert html.challenge_type == "practical"
        assert html.evidence_required is True
        assert html.rubric == "html-quality"

    def test_mission_prerequisites(self, cyber_pkg):
        web = next(j for j in cyber_pkg.journeys if j.id == "fundamentos-web")
        css = next(m for m in web.missions if m.id == "css-foundations")
        assert css.prerequisites == ["html-foundations"]

    def test_logica_programacao_has_one_mission(self, cyber_pkg):
        logica = next(j for j in cyber_pkg.journeys if j.id == "logica-programacao")
        assert len(logica.missions) == 1
        assert logica.missions[0].id == "python-basics"

    def test_journey_unlocks(self, cyber_pkg):
        web = next(j for j in cyber_pkg.journeys if j.id == "fundamentos-web")
        assert web.unlocks == ["logica-programacao"]
        logica = next(j for j in cyber_pkg.journeys if j.id == "logica-programacao")
        assert logica.unlocks == []

    def test_rubric_criteria_weights(self, cyber_pkg):
        html_rubric = next(r for r in cyber_pkg.rubrics if r.id == "html-quality")
        total = sum(c.weight for c in html_rubric.criteria.values())
        assert total == 100

    def test_competency_levels(self, cyber_pkg):
        for c in cyber_pkg.competencies:
            assert c.level == "beginner"
        html = next(c for c in cyber_pkg.competencies if c.id == "html-fundamental")
        assert html.mastery_threshold == 80


class TestValidator:
    def test_valid_package_passes(self, validator, cyber_pkg):
        result = validator.validate(cyber_pkg)
        assert result.valid is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 0

    def test_missing_package_id(self, validator):
        pkg = Package(id="", version="1.0")
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "missing-id" for e in result.errors)

    def test_missing_version(self, validator):
        pkg = Package(id="test", version="")
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "missing-version" for e in result.errors)

    def test_no_content_warning(self, validator):
        pkg = Package(id="empty", version="1.0")
        result = validator.validate(pkg)
        assert result.valid is True
        assert any(e.rule == "no-content" for e in result.warnings)

    def test_negative_xp(self, validator):
        pkg = Package(id="test", version="1.0")
        j = Journey(id="j1", missions=[Mission(id="m1", xp=-50)])
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "negative-xp" for e in result.errors)

    def test_competency_not_found(self, validator):
        pkg = Package(id="test", version="1.0")
        pkg.competencies = [CompetencyDef(id="real-comp", name="Real")]
        j = Journey(id="j1", missions=[Mission(id="m1", competencies=["missing-comp"])])
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "competency-not-found" for e in result.errors)

    def test_journey_unlock_not_found(self, validator):
        pkg = Package(id="test", version="1.0")
        j = Journey(id="j1", unlocks=["non-existent-journey"])
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "journey-unlock-not-found" for e in result.errors)

    def test_duplicate_mission_id(self, validator):
        pkg = Package(id="test", version="1.0")
        j = Journey(
            id="j1",
            missions=[
                Mission(id="dup"),
                Mission(id="dup"),
            ],
        )
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "duplicate-mission-id" for e in result.errors)

    def test_rubric_not_found_warning(self, validator):
        pkg = Package(id="test", version="1.0")
        j = Journey(id="j1", missions=[Mission(id="m1", rubric="non-existent-rubric")])
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is True
        assert any(e.rule == "rubric-not-found" for e in result.warnings)

    def test_rubric_weights_not_100_warning(self, validator):
        pkg = Package(id="test", version="1.0")
        pkg.rubrics = [
            Rubric(
                id="r1",
                criteria={
                    "a": RubricCriterion(weight=30),
                    "b": RubricCriterion(weight=30),
                },
            )
        ]
        result = validator.validate(pkg)
        assert result.valid is True
        assert any(e.rule == "rubric-weights" for e in result.warnings)

    def test_prerequisite_not_found(self, validator):
        pkg = Package(id="test", version="1.0")
        j = Journey(
            id="j1",
            missions=[Mission(id="m1", prerequisites=["ghost-mission"])],
        )
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "prerequisite-not-found" for e in result.errors)

    def test_mission_no_id(self, validator):
        pkg = Package(id="test", version="1.0")
        j = Journey(id="j1", missions=[Mission(id="")])
        pkg.journeys.append(j)
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "mission-no-id" for e in result.errors)

    def test_journey_no_id(self, validator):
        pkg = Package(id="test", version="1.0")
        pkg.journeys.append(Journey(id=""))
        result = validator.validate(pkg)
        assert result.valid is False
        assert any(e.rule == "journey-no-id" for e in result.errors)


class TestLoader:
    def test_load_and_validate_returns_package(self, loader):
        pkg = loader.load_and_validate(PACKAGES_DIR / "cyber-foundations")
        assert isinstance(pkg, Package)
        assert pkg.id == "cyber-foundations"

    def test_load_and_validate_raises_on_invalid(self, loader, tmp_path):
        pkg_dir = tmp_path / "bad-pkg"
        pkg_dir.mkdir()
        (pkg_dir / "package.yaml").write_text(
            "metadata:\n  id: ''\n  version: ''\n", encoding="utf-8"
        )
        with pytest.raises(ValueError, match="Package validation failed"):
            loader.load_and_validate(pkg_dir)

    def test_load_returns_result(self, loader):
        pkg, result = loader.load(PACKAGES_DIR / "cyber-foundations")
        assert isinstance(pkg, Package)
        assert isinstance(result, ValidationResult)
        assert result.valid is True

    def test_load_missing_yaml_returns_errors(self, loader, tmp_path):
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        (empty_dir / "package.yaml").write_text(
            "metadata:\n  id: 'test'\n  version: '1.0'\n", encoding="utf-8"
        )
        pkg, result = loader.load(empty_dir)
        assert pkg.id == "test"
        assert result.valid is True
        assert len(pkg.journeys) == 0


class TestIntegration:
    def test_full_roundtrip(self, loader):
        pkg, result = loader.load(PACKAGES_DIR / "cyber-foundations")
        assert result.valid is True

        assert len(pkg.competencies) == 3
        assert len(pkg.achievements) == 2
        assert len(pkg.rubrics) == 2
        assert len(pkg.journeys) == 2

        total_missions = sum(len(j.missions) for j in pkg.journeys)
        assert total_missions == 3

    def test_invalid_package_rejected(self, loader, tmp_path):
        pkg_dir = tmp_path / "invalid"
        pkg_dir.mkdir()
        (pkg_dir / "package.yaml").write_text(
            "metadata:\n  id: inv\n  version: 1.0\n", encoding="utf-8"
        )
        j_dir = pkg_dir / "journeys" / "j1"
        j_dir.mkdir(parents=True)
        (j_dir / "journey.yaml").write_text(
            "metadata:\n  id: j1\n\nspec:\n  unlocks:\n    - ghost-journey\n",
            encoding="utf-8",
        )
        _, result = loader.load(pkg_dir)
        assert result.valid is False
        assert any(e.rule == "journey-unlock-not-found" for e in result.errors)
