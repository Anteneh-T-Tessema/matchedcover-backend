""""
Policies API endpoints for MatchedCover Insurance Platform.
""""

from typing import Dict
from fastapi import APIRouter, Depends
from src.api.auth import get_current_user

router = APIRouter()


@router.get("/")
async def list_policies(current_user: Dict = Depends(get_current_user)):
    """Get list of policies."""
return {"policies": [], "total": 0}
