from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.block_repo import block_repo
from app.schemas.block_schema import BlockResponse, BlockListResponse

class BlockService:
    def block_user(self, db: Session, me_id: str, user_id: str) -> BlockResponse:
        if me_id == user_id:
            raise HTTPException(status_code=400, detail="Cannot block yourself")
        if block_repo.has_blocked_user(db, me_id, user_id):
            raise HTTPException(status_code=400, detail="Already blocked")
        block = block_repo.block_user(db, me_id, user_id)
        return BlockResponse.model_validate(block)

    def unblock_user(self, db: Session, me_id: str, user_id: str):
        if me_id == user_id:
            raise HTTPException(status_code=400, detail="Cannot unblock yourself")
        success = block_repo.unblock_user(db, me_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Block not found")

        return {"success": True}

    def list_blocked_users(self, db: Session, me_id: str) -> BlockListResponse:
        users = block_repo.list_blocked_users(db, me_id)
        return BlockListResponse(blocked_users=users)

    def is_blocked_by_user(self, db: Session, me_id: str, user_id: str) -> bool:
        return block_repo.is_blocked_by_user(db, me_id, user_id)

    def has_blocked_user(self, db: Session, me_id: str, user_id: str) -> bool:
        return block_repo.has_blocked_user(db, me_id, user_id)


block_service = BlockService()