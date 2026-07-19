from pathlib import Path
from typing import Any

from .models import (
    AchievementDef,
    CompetencyDef,
    Journey,
    Mission,
    Package,
    Rubric,
    RubricCriterion,
)


class PackageParser:
    def parse_package(self, data: dict) -> Package:
        meta = data.get("metadata", {})
        spec = data.get("spec", {})
        caps = data.get("capabilities", ["evidence"])
        return Package(
            id=meta.get("id", ""),
            version=meta.get("version", "0.0.0"),
            title=meta.get("title", ""),
            description=meta.get("description", ""),
            author=meta.get("author", ""),
            license=meta.get("license", ""),
            runtime=spec.get("runtime", ">=1.0"),
            language=spec.get("language", "en"),
            estimated_hours=spec.get("estimated_hours", 0),
            dependencies=spec.get("dependencies", []),
            capabilities=caps,
        )

    def parse_journey(self, data: dict) -> Journey:
        meta = data.get("metadata", {})
        spec = data.get("spec", {})
        return Journey(
            id=meta.get("id", ""),
            title=meta.get("title", ""),
            description=meta.get("description", ""),
            difficulty=spec.get("difficulty", "beginner"),
            estimated_hours=spec.get("estimated_hours", 10),
            unlocks=spec.get("unlocks", []),
        )

    def parse_mission(self, data: dict) -> Mission:
        meta = data.get("metadata", {})
        spec = data.get("spec", {})
        challenge = spec.get("challenge", {})
        evidence = spec.get("evidence", {})
        assessment = spec.get("assessment", {})
        return Mission(
            id=meta.get("id", ""),
            title=meta.get("title", ""),
            difficulty=spec.get("difficulty", "beginner"),
            estimated_minutes=spec.get("estimated_minutes", 60),
            xp=spec.get("xp", 100),
            prerequisites=spec.get("prerequisites", []),
            competencies=spec.get("competencies", []),
            challenge_type=challenge.get("type", "practical"),
            challenge_description=challenge.get("description", ""),
            evidence_required=evidence.get("required", True),
            evidence_types=evidence.get("types", ["code", "document"]),
            rubric=assessment.get("rubric", ""),
        )

    def parse_competencies(self, data: dict) -> list[CompetencyDef]:
        spec = data.get("spec", {})
        return [
            CompetencyDef(
                id=c.get("id", ""),
                name=c.get("name", ""),
                description=c.get("description", ""),
                level=c.get("level", "beginner"),
                evidence_required=c.get("evidence_required", True),
                mastery_threshold=c.get("mastery_threshold", 80),
            )
            for c in spec.get("competencies", [])
        ]

    def parse_achievements(self, data: dict) -> list[AchievementDef]:
        spec = data.get("spec", {})
        return [
            AchievementDef(
                id=a.get("id", ""),
                name=a.get("name", ""),
                description=a.get("description", ""),
                criteria=a.get("criteria", []),
                badge=a.get("badge", ""),
            )
            for a in spec.get("achievements", [])
        ]

    def parse_rubrics(self, data: dict) -> list[Rubric]:
        spec = data.get("spec", {})
        result = []
        for r in spec.get("rubrics", []):
            criteria = {}
            for cid, cdata in r.get("criteria", {}).items():
                criteria[cid] = RubricCriterion(
                    weight=cdata.get("weight", 0),
                    description=cdata.get("description", ""),
                )
            result.append(
                Rubric(
                    id=r.get("id", ""),
                    title=r.get("title", ""),
                    criteria=criteria,
                )
            )
        return result

    def load_yaml(self, path: Path) -> dict:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
