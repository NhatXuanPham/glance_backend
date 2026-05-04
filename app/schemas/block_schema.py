from pydantic import BaseModel, UUID4
from datetime import datetime

class BlockUserRequest(BaseModel):
    blocked_id: UUID4

class UnblockUserRequest(BaseModel):
    blocked_id: UUID4

class BlockResponse(BaseModel):
    blocker_id: UUID4
    blocked_id: UUID4
    created_at: datetime

    class Config:
        from_attributes = True  

class BlockListResponse(BaseModel):
    blocked_users: list[UUID4]

class BlockStatusResponse(BaseModel):
    is_blocked: bool