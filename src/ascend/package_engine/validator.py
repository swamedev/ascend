from dataclasses import dataclass, field
from typing import List

from .models import Package


@dataclass
class ValidationIssue:
    rule: str
    path: str
    message: str
    level: str = "error"


@dataclass
class ValidationResult:
    valid: bool = True
    errors: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)

    def add_error(self, rule: str, path: str, message: str) -> None:
        self.errors.append(ValidationIssue(rule, path, message, "error"))
        self.valid = False

    def add_warning(self, rule: str, path: str, message: str) -> None:
        self.warnings.append(ValidationIssue(rule, path, message, "warning"))


class PackageValidator:
    def validate(self, pkg: Package) -> ValidationResult:
        result = ValidationResult()

        self._validate_metadata(pkg, result)
        self._validate_journeys(pkg, result)
        self._validate_competencies(pkg, result)
        self._validate_missions(pkg, result)
        self._validate_rubrics(pkg, result)
        self._validate_xp(pkg, result)
        self._validate_prerequisites(pkg, result)

        return result

    def _validate_metadata(self, pkg: Package, result: ValidationResult) -> None:
        if not pkg.id:
            result.add_error("missing-id", "package.yaml", "Package ID is required")
        if not pkg.version:
            result.add_error("missing-version", "package.yaml", "Version is required")
        if not pkg.journeys and not pkg.competencies:
            result.add_warning(
                "no-content", "package.yaml", "Package has no journeys or competencies"
            )

    def _validate_journeys(self, pkg: Package, result: ValidationResult) -> None:
        journey_ids = {j.id for j in pkg.journeys}
        for j in pkg.journeys:
            if not j.id:
                result.add_error("journey-no-id", "journeys/", "Journey without ID")
            for unlock in j.unlocks:
                if unlock not in journey_ids:
                    result.add_error(
                        "journey-unlock-not-found",
                        f"journeys/{j.id}/journey.yaml",
                        f"Unlock '{unlock}' not found in package journeys",
                    )

    def _validate_competencies(
        self, pkg: Package, result: ValidationResult
    ) -> None:
        comp_ids = {c.id for c in pkg.competencies}
        for j in pkg.journeys:
            for m in j.missions:
                for cid in m.competencies:
                    if cid not in comp_ids:
                        result.add_error(
                            "competency-not-found",
                            f"journeys/{j.id}/missions/{m.id}/mission.yaml",
                            f"Competency '{cid}' not defined in competencies.yaml",
                        )

    def _validate_missions(self, pkg: Package, result: ValidationResult) -> None:
        for j in pkg.journeys:
            seen = set()
            for m in j.missions:
                if not m.id:
                    result.add_error(
                        "mission-no-id",
                        f"journeys/{j.id}/missions/",
                        "Mission without ID",
                    )
                if m.id in seen:
                    result.add_error(
                        "duplicate-mission-id",
                        f"journeys/{j.id}/missions/{m.id}",
                        f"Duplicate mission ID '{m.id}'",
                    )
                seen.add(m.id)

    def _validate_rubrics(self, pkg: Package, result: ValidationResult) -> None:
        rubric_ids = {r.id for r in pkg.rubrics}
        for j in pkg.journeys:
            for m in j.missions:
                if m.rubric and m.rubric not in rubric_ids:
                    result.add_warning(
                        "rubric-not-found",
                        f"journeys/{j.id}/missions/{m.id}/mission.yaml",
                        f"Rubric '{m.rubric}' not defined in rubrics.yaml",
                    )
        for r in pkg.rubrics:
            total = sum(c.weight for c in r.criteria.values())
            if total != 100:
                result.add_warning(
                    "rubric-weights",
                    f"assessments/rubrics.yaml",
                    f"Rubric '{r.id}' weights sum to {total}, expected 100",
                )

    def _validate_xp(self, pkg: Package, result: ValidationResult) -> None:
        for j in pkg.journeys:
            for m in j.missions:
                if m.xp < 0:
                    result.add_error(
                        "negative-xp",
                        f"journeys/{j.id}/missions/{m.id}",
                        f"XP cannot be negative: {m.xp}",
                    )

    def _validate_prerequisites(
        self, pkg: Package, result: ValidationResult
    ) -> None:
        for j in pkg.journeys:
            mission_ids = {m.id for m in j.missions}
            for m in j.missions:
                for prereq in m.prerequisites:
                    if prereq not in mission_ids:
                        result.add_error(
                            "prerequisite-not-found",
                            f"journeys/{j.id}/missions/{m.id}",
                            f"Prerequisite '{prereq}' not found in journey '{j.id}'",
                        )
