from dataclasses import dataclass, field
from typing import List


@dataclass
class RuntimeChallenge:
    type: str
    description: str
    evidence_required: bool
    evidence_types: List[str]


@dataclass
class RuntimeMission:
    id: str
    title: str
    description: str
    difficulty: str
    estimated_minutes: int
    xp: int
    prerequisites: List[str]
    competencies: List[str]
    challenge: RuntimeChallenge
    rubric_id: str


@dataclass
class RuntimeJourney:
    id: str
    title: str
    description: str
    difficulty: str
    estimated_hours: int
    missions: List[RuntimeMission]
    unlocks: List[str]


@dataclass
class RuntimeCompetency:
    id: str
    name: str
    description: str
    level: str
    evidence_required: bool
    mastery_threshold: int


@dataclass
class RuntimeCriterion:
    weight: int
    description: str


@dataclass
class RuntimeRubric:
    id: str
    title: str
    criteria: dict[str, RuntimeCriterion]


@dataclass
class RuntimeAchievement:
    id: str
    name: str
    description: str
    criteria: List[str]
    badge: str


@dataclass
class RuntimePackage:
    id: str
    version: str
    title: str
    description: str
    author: str
    journeys: List[RuntimeJourney]
    competencies: dict[str, RuntimeCompetency]
    rubrics: dict[str, RuntimeRubric]
    achievements: dict[str, RuntimeAchievement]
    dependencies: List[str]
    capabilities: List[str]
