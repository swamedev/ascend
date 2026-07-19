from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RubricCriterion:
    weight: int
    description: str = ""


@dataclass
class Rubric:
    id: str
    title: str = ""
    criteria: dict[str, RubricCriterion] = field(default_factory=dict)


@dataclass
class CompetencyDef:
    id: str
    name: str = ""
    description: str = ""
    level: str = "beginner"
    evidence_required: bool = True
    mastery_threshold: int = 80


@dataclass
class AchievementDef:
    id: str
    name: str = ""
    description: str = ""
    criteria: List[str] = field(default_factory=list)
    badge: str = ""


@dataclass
class Mission:
    id: str
    title: str = ""
    difficulty: str = "beginner"
    estimated_minutes: int = 60
    xp: int = 100
    prerequisites: List[str] = field(default_factory=list)
    competencies: List[str] = field(default_factory=list)
    challenge_type: str = "practical"
    challenge_description: str = ""
    evidence_required: bool = True
    evidence_types: List[str] = field(default_factory=lambda: ["code", "document"])
    rubric: str = ""


@dataclass
class Journey:
    id: str
    title: str = ""
    description: str = ""
    difficulty: str = "beginner"
    estimated_hours: int = 10
    missions: List[Mission] = field(default_factory=list)
    unlocks: List[str] = field(default_factory=list)


@dataclass
class Package:
    id: str
    version: str
    title: str = ""
    description: str = ""
    author: str = ""
    license: str = ""
    runtime: str = ">=1.0"
    language: str = "en"
    estimated_hours: int = 0
    journeys: List[Journey] = field(default_factory=list)
    competencies: List[CompetencyDef] = field(default_factory=list)
    achievements: List[AchievementDef] = field(default_factory=list)
    rubrics: List[Rubric] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=lambda: ["evidence"])
