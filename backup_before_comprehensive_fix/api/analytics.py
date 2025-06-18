""""
Analytics API endpoints for MatchedCover Insurance Platform.
""""

from typing import Dict
from fastapi import APIRouter, Depends
from src.api.auth import get_current_user

router = APIRouter()


@router.get("/overview")
async def get_analytics_overview(
    current_user: Dict = Depends(get_current_user),
):
    """Get analytics overview."""
return {
    "total_customers": 15432,
    "active_policies": 23567,
    "pending_claims": 342,
    "revenue_this_month": 2547890.50,
}
