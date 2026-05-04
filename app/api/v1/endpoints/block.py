from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.block_service import block_service
from app.core.security import verify_access_token
from app.schemas.block_schema import BlockResponse, BlockListResponse

router = APIRouter(tags=["blocks"])

@router.post("/blocks/{user_id}", response_model=BlockResponse, status_code=status.HTTP_201_CREATED)
def block_user(
    user_id: str,
    db: Session = Depends(get_db),
    payload=Depends(verify_access_token),
):
    return block_service.block_user(db, str(payload["sub"]), user_id)

@router.delete("/unblocks/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def unblock_user(
    user_id: str,
    db: Session = Depends(get_db),
    payload=Depends(verify_access_token),
):
    block_service.unblock_user(db, str(payload["sub"]), user_id)

@router.get("/list_blocked", response_model=BlockListResponse)
def list_blocked_users(
    db: Session = Depends(get_db),
    payload=Depends(verify_access_token),
):
    return block_service.list_blocked_users(db, str(payload["sub"]))