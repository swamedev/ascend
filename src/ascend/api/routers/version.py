"""Version endpoint."""

from fastapi import APIRouter

from ascend.api.version import VERSIONS

router = APIRouter(tags=["version"])


@router.get("/version")
def get_version() -> dict:
    return VERSIONS
