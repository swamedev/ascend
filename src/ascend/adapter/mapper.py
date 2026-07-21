"""Domain entity → Canonical Contract mappers.

Each function converts a Runtime domain entity into a Python dict
that matches the @ascend/contracts TypeScript interface shape.

These dicts are JSON-serializable and ready for API transport.
"""

from datetime import datetime
from typing import Any

from ascend.domain.achievement import Achievement
from ascend.domain.assessment import Assessment
from ascend.domain.builder import Builder
from ascend.domain.competency import Competency
from ascend.domain.evidence import Evidence
from ascend.domain.journey import Journey
from ascend.domain.mission import Mission


def builder_to_canonical(builder: Builder) -> dict[str, Any]:
    competencies = [c for c in builder.competencies]
    achievements = [a for a in builder.achievements]
    evidence_list = [e for e in builder.evidence_list]
    active_missions = [m for m in builder.active_missions]
    completed_missions = [m for m in builder.completed_missions]

    return {
        "id": builder.id,
        "profile": {
            "name": builder.username,
            "avatar": None,
            "bio": None,
            "email": None,
            "socialLinks": None,
        },
        "preferences": {
            "theme": "system",
            "language": "en",
            "reducedMotion": False,
            "fontSize": "medium",
            "notifications": {
                "email": True,
                "push": True,
                "digest": "daily",
                "mentions": True,
                "achievements": True,
            },
            "privacy": {
                "profileVisibility": "public",
                "showXP": True,
                "showStreak": True,
                "showCompetencies": True,
                "showAchievements": True,
            },
        },
        "identity": learning_identity_to_canonical(
            builder, competencies, evidence_list, achievements
        ),
        "ledger": ledger_to_canonical(builder, achievements),
        "progress": progress_to_canonical(
            builder, active_missions, completed_missions
        ),
        "createdAt": _iso_now(),
        "updatedAt": _iso_now(),
        "deletedAt": None,
    }


def learning_identity_to_canonical(
    builder: Builder,
    competencies: list[Competency],
    evidence_list: list[Evidence],
    achievements: list[Achievement],
) -> dict[str, Any]:
    accepted = [e for e in evidence_list if e.status.value == "accepted"]
    pending = [e for e in evidence_list if e.status.value == "submitted"]

    return {
        "builderId": builder.id,
        "competencies": {
            "nodes": [competency_node_to_canonical(c) for c in competencies],
            "edges": [],
            "lastUpdated": _iso_now(),
        },
        "evidence": {
            "totalCount": len(evidence_list),
            "acceptedCount": len(accepted),
            "pendingCount": len(pending),
            "items": [
                evidence_summary_to_canonical(e) for e in evidence_list
            ],
        },
        "assessments": {
            "totalTaken": 0,
            "passed": 0,
            "failed": 0,
            "averageScore": 0.0,
            "recentResults": [],
        },
        "learningPath": {
            "completedJourneys": [],
            "inProgressJourneys": [],
            "availableJourneys": [],
            "suggestedNext": [],
        },
        "exportedAt": None,
    }


def competency_node_to_canonical(comp: Competency) -> dict[str, Any]:
    return {
        "id": comp.id,
        "name": comp.name,
        "category": "general",
        "currentLevel": comp.level,
        "maxLevel": 5,
        "progress": min(comp.level / 5.0, 1.0),
        "unlockedAt": _iso_now(),
        "evidenceIds": [],
    }


def evidence_summary_to_canonical(evidence: Evidence) -> dict[str, Any]:
    return {
        "id": evidence.id,
        "missionId": evidence.mission_id,
        "type": evidence.type.value,
        "status": _map_evidence_status(evidence.status.value),
        "submittedAt": (
            evidence.submitted_at.isoformat()
            if evidence.submitted_at
            else _iso_now()
        ),
        "competencies": [],
    }


def ledger_to_canonical(
    builder: Builder, achievements: list[Achievement]
) -> dict[str, Any]:
    return {
        "builderId": builder.id,
        "entries": [
            ledger_entry_to_canonical(a) for a in achievements
        ],
        "totalAchievements": len(achievements),
        "totalCertificates": 0,
        "lastUpdated": _iso_now(),
    }


def ledger_entry_to_canonical(achievement: Achievement) -> dict[str, Any]:
    return {
        "id": achievement.id,
        "type": "achievement",
        "ref": achievement.id,
        "title": achievement.name,
        "description": achievement.description,
        "grantedAt": (
            achievement.earned_at.isoformat()
            if achievement.earned_at
            else _iso_now()
        ),
        "source": "journey",
        "expiresAt": None,
        "metadata": None,
        "verifiable": False,
    }


def progress_to_canonical(
    builder: Builder,
    active_missions: list[Mission],
    completed_missions: list[Mission],
) -> dict[str, Any]:
    next_level_xp = ((builder.level + 1) * 500) if builder.level < 100 else builder.xp
    return {
        "builderId": builder.id,
        "level": builder.level,
        "xp": {
            "current": builder.xp,
            "total": sum(m.xp_reward for m in completed_missions),
            "nextLevelAt": next_level_xp,
            "history": [],
        },
        "streak": {
            "current": 0,
            "longest": 0,
            "lastActivity": _iso_now(),
            "frozen": False,
            "freezeAvailable": 0,
        },
        "timeline": [],
        "stats": {
            "missionsCompleted": len(completed_missions),
            "evidenceSubmitted": len(builder.evidence_list),
            "evidenceAccepted": len(
                [e for e in builder.evidence_list if e.status.value == "accepted"]
            ),
            "achievementsUnlocked": len(builder.achievements),
            "competenciesUnlocked": len(builder.competencies),
            "journeysCompleted": 0,
            "assessmentsPassed": 0,
            "activeDays": 0,
            "joinDate": _iso_now(),
        },
    }


def journey_to_summary(journey: Journey) -> dict[str, Any]:
    missions = journey.missions
    completed = [m for m in missions if m.is_completed]
    return {
        "id": journey.id,
        "title": journey.name,
        "description": journey.objective,
        "category": "general",
        "difficulty": 1,
        "estimatedDuration": "",
        "missionCount": len(missions),
        "completedCount": len(completed),
        "status": _map_journey_status(journey.status.value),
        "xpReward": sum(m.xp_reward for m in missions),
        "prerequisites": [],
    }


def journey_to_detail(journey: Journey) -> dict[str, Any]:
    missions = journey.missions
    completed = [m for m in missions if m.is_completed]
    return {
        "id": journey.id,
        "title": journey.name,
        "description": journey.objective,
        "category": "general",
        "difficulty": 1,
        "estimatedDuration": "",
        "xpReward": sum(m.xp_reward for m in missions),
        "certificateId": None,
        "prerequisites": [],
        "missions": [mission_to_summary(m) for m in missions],
        "status": _map_journey_status(journey.status.value),
        "progress": {
            "journeyId": journey.id,
            "builderId": "",
            "missionsCompleted": len(completed),
            "missionsTotal": len(missions),
            "evidenceSubmitted": 0,
            "evidenceAccepted": 0,
            "xpEarned": sum(m.xp_reward for m in completed),
            "percentComplete": (
                (len(completed) / len(missions) * 100) if missions else 0
            ),
            "startedAt": _iso_now(),
            "completedAt": None,
            "lastActivityAt": _iso_now(),
        },
        "startedAt": None,
        "completedAt": None,
    }


def mission_to_summary(mission: Mission) -> dict[str, Any]:
    evidence_submitted = len(mission.evidence_list)
    return {
        "id": mission.id,
        "title": mission.title,
        "description": mission.objective,
        "type": "challenge",
        "status": _map_mission_status(mission.status.value),
        "xpReward": mission.xp_reward,
        "evidenceRequired": 1,
        "evidenceSubmitted": evidence_submitted,
        "prerequisites": mission.prerequisites,
    }


def mission_to_detail(
    mission: Mission, journey_id: str = ""
) -> dict[str, Any]:
    return {
        "id": mission.id,
        "journeyId": journey_id,
        "title": mission.title,
        "description": mission.objective,
        "type": "challenge",
        "instructions": mission.objective,
        "xpReward": mission.xp_reward,
        "evidenceRequired": 1,
        "prerequisites": mission.prerequisites,
        "status": _map_mission_status(mission.status.value),
        "startedAt": _iso_now() if mission.is_active else None,
        "completedAt": _iso_now() if mission.is_completed else None,
    }


def evidence_to_record(evidence: Evidence) -> dict[str, Any]:
    return {
        "id": evidence.id,
        "missionId": evidence.mission_id,
        "builderId": evidence.builder_id,
        "type": evidence.type.value,
        "content": evidence.artifact,
        "status": _map_evidence_status(evidence.status.value),
        "submittedAt": (
            evidence.submitted_at.isoformat()
            if evidence.submitted_at
            else _iso_now()
        ),
        "reviewedAt": None,
        "feedback": None,
        "competencies": [],
    }


def assessment_to_result(
    assessment: Assessment, title: str = ""
) -> dict[str, Any]:
    return {
        "assessmentId": assessment.id,
        "title": title,
        "score": assessment.score,
        "total": 100,
        "passed": assessment.is_approved,
        "completedAt": assessment.created_at.isoformat(),
    }


def competency_to_summary(comp: Competency) -> dict[str, Any]:
    return {
        "id": comp.id,
        "name": comp.name,
        "category": "general",
        "level": comp.level,
        "maxLevel": 5,
        "progress": min(comp.level / 5.0, 1.0),
        "status": "completed" if comp.level > 0 else "available",
    }


def competency_to_detail(comp: Competency) -> dict[str, Any]:
    return {
        "id": comp.id,
        "name": comp.name,
        "category": "general",
        "description": comp.description,
        "level": comp.level,
        "maxLevel": 5,
        "progress": min(comp.level / 5.0, 1.0),
        "status": "completed" if comp.level > 0 else "available",
        "prerequisites": [],
        "unlockedAt": _iso_now(),
        "evidenceIds": [],
        "children": [],
    }


def achievement_to_summary(achievement: Achievement) -> dict[str, Any]:
    return {
        "id": achievement.id,
        "name": achievement.name,
        "description": achievement.description,
        "category": "general",
        "rarity": "common",
        "icon": None,
        "grantedAt": (
            achievement.earned_at.isoformat()
            if achievement.earned_at
            else None
        ),
        "progress": 100 if achievement.is_earned else 0,
        "maxProgress": 100,
    }


def _map_mission_status(status: str) -> str:
    mapping = {
        "available": "available",
        "started": "in_progress",
        "evidence_submitted": "in_progress",
        "completed": "completed",
    }
    return mapping.get(status, "available")


def _map_journey_status(status: str) -> str:
    mapping = {
        "locked": "locked",
        "available": "available",
        "active": "in_progress",
        "completed": "completed",
    }
    return mapping.get(status, "available")


def _map_evidence_status(status: str) -> str:
    mapping = {
        "submitted": "pending",
        "accepted": "accepted",
        "rejected": "rejected",
    }
    return mapping.get(status, "pending")


def _iso_now() -> str:
    return datetime.now().isoformat()
