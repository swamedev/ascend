"""Pydantic v2 schemas for the Builder resource."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class BuilderCreate(BaseModel):
    username: str = Field(
        ..., min_length=2, max_length=64, description="Unique builder identifier"
    )
    display_name: str | None = Field(
        None, max_length=128, description="Public display name"
    )


class BuilderUpdate(BaseModel):
    display_name: str | None = Field(None, max_length=128)
    bio: str | None = Field(None, max_length=512)


# ---------------------------------------------------------------------------
# Response models — full canonical shapes
# ---------------------------------------------------------------------------


class ProfileOut(BaseModel):
    name: str
    avatar: str | None = None
    bio: str | None = None
    email: str | None = None
    socialLinks: list | None = None


class PreferencesOut(BaseModel):
    theme: str = "system"
    language: str = "en"
    reducedMotion: bool = False
    fontSize: str = "medium"


class CompetencyNodeOut(BaseModel):
    id: str
    name: str
    category: str
    currentLevel: int
    maxLevel: int
    progress: float
    unlockedAt: str | None = None
    evidenceIds: list[str] = []


class EvidenceSummaryOut(BaseModel):
    id: str
    missionId: str
    type: str
    status: str
    submittedAt: str
    competencies: list[str] = []


class EvidencePortfolioOut(BaseModel):
    totalCount: int = 0
    acceptedCount: int = 0
    pendingCount: int = 0
    items: list[EvidenceSummaryOut] = []


class AssessmentResultOut(BaseModel):
    assessmentId: str
    title: str
    score: float
    total: float
    passed: bool
    completedAt: str


class CompetencyGraphOut(BaseModel):
    nodes: list[CompetencyNodeOut] = []
    edges: list = []
    lastUpdated: str = ""


class LearningIdentityOut(BaseModel):
    builderId: str
    competencies: CompetencyGraphOut
    evidence: EvidencePortfolioOut
    assessments: dict = {}
    learningPath: dict = {}
    exportedAt: str | None = None


class LedgerEntryOut(BaseModel):
    id: str
    type: str
    ref: str
    title: str
    description: str
    grantedAt: str
    source: str
    expiresAt: str | None = None
    metadata: dict[str, Any] | None = None
    verifiable: bool = False


class AchievementLedgerOut(BaseModel):
    builderId: str
    entries: list[LedgerEntryOut] = []
    totalAchievements: int = 0
    totalCertificates: int = 0
    lastUpdated: str = ""


class XPEventOut(BaseModel):
    amount: int
    source: str
    description: str
    timestamp: str


class XPMetricsOut(BaseModel):
    current: int = 0
    total: int = 0
    nextLevelAt: int = 0
    history: list[XPEventOut] = []


class StreakMetricsOut(BaseModel):
    current: int = 0
    longest: int = 0
    lastActivity: str = ""
    frozen: bool = False
    freezeAvailable: int = 0


class BuilderStatsOut(BaseModel):
    missionsCompleted: int = 0
    evidenceSubmitted: int = 0
    evidenceAccepted: int = 0
    achievementsUnlocked: int = 0
    competenciesUnlocked: int = 0
    journeysCompleted: int = 0
    assessmentsPassed: int = 0
    activeDays: int = 0
    joinDate: str = ""


class BuilderProgressOut(BaseModel):
    builderId: str
    level: int = 1
    xp: XPMetricsOut = XPMetricsOut()
    streak: StreakMetricsOut = StreakMetricsOut()
    timeline: list = []
    stats: BuilderStatsOut = BuilderStatsOut()


class BuilderOut(BaseModel):
    id: str
    profile: ProfileOut
    preferences: PreferencesOut
    identity: LearningIdentityOut
    ledger: AchievementLedgerOut
    progress: BuilderProgressOut
    createdAt: str
    updatedAt: str
    deletedAt: str | None = None
