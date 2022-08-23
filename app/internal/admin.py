#!/urs/bin/env python3

from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def update_admin():
    return {"message": "ADmin page"}
