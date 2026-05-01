import httpx
import uuid
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import (
    create_token,
    hash_password,
    verify_password,
)
from app.db.models.users import User
from app.repositories.user_repo import user_repo
from app.repositories.token_repo import refresh_token_repo
from app.schemas.auth_schema import AccessTokenResponse, RegisterRequest

class AuthService:

    def register(self, db: Session, data: RegisterRequest) -> User:
        if user_repo.get_by_email(db, data.email):
            raise HTTPException(status_code=400, detail="Email đã được sử dụng")
        if user_repo.get_by_username(db, data.username):
            raise HTTPException(status_code=400, detail="Username đã được sử dụng")

        return user_repo.create(
            db,
            display_name=data.display_name,
            username=data.username,
            email=data.email,
            password_hash=hash_password(data.password),
        )

    def login(self, db: Session, form_data: OAuth2PasswordRequestForm) -> AccessTokenResponse:
        user = user_repo.get_by_email(db, form_data.username)
        if not user or not verify_password(form_data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không đúng")
        if not user.active:
            raise HTTPException(status_code=403, detail="Tài khoản đã bị vô hiệu hóa")

        return self._issue_tokens(db, user)

    def logout(self, db: Session, refresh_token: str) -> None:
        rt = refresh_token_repo.get_by_token(db, refresh_token)
        if not rt or rt.revoked:
            raise HTTPException(status_code=400, detail="Refresh token không hợp lệ")
        refresh_token_repo.revoke(db, refresh_token)

    def logout_all(self, db: Session, user_id: uuid.UUID) -> None:
        refresh_token_repo.revoke_all_by_user(db, user_id)

    def google_callback(self, db: Session, code: str) -> AccessTokenResponse:
        google_access_token = self._exchange_code(code)
        user_info = self._get_google_user(google_access_token)

        email = user_info["email"]
        user = user_repo.get_by_email(db, email)

        if not user:
            user = user_repo.create(
                db,
                display_name=user_info.get("name", email.split("@")[0]),
                username=email.split("@")[0] + "_" + str(uuid.uuid4())[:6],
                email=email,
                password_hash=None,
                avatar_url=user_info.get("picture"),
            )

        return self._issue_tokens(db, user)

    def get_profile(self, db: Session, user_id: uuid.UUID) -> User:
        user = user_repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User không tìm thấy")
        return user

    def _issue_tokens(self, db: Session, user: User) -> AccessTokenResponse:
        access_token, expires_at = create_token(user.id, "access")
        refresh_token, expires_at = create_token(user.id, "refresh")
        refresh_token_repo.create(db, user.id, refresh_token, expires_at)
        return AccessTokenResponse(access_token=access_token, refresh_token=refresh_token)

    def _exchange_code(self, code: str) -> str:
        response = httpx.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        data = response.json()
        if "error" in data:
            raise HTTPException(status_code=400, detail="Google OAuth thất bại")
        return data["access_token"]

    def _get_google_user(self, access_token: str) -> dict:
        response = httpx.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        return response.json()


auth_service = AuthService()