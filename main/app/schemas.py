from pydantic import BaseModel, ConfigDict, EmailStr

from app.models import User


class BaseSchema(BaseModel, frozen=True):
    model_config = ConfigDict(extra="forbid")


class CreateNewUserPayload(BaseSchema):
    user_uid: str
    user_email: EmailStr


class UserSchema(BaseSchema):
    google_identity_uid: str
    email: EmailStr

    @classmethod
    def from_orm(cls, user: User) -> "UserSchema":
        return UserSchema(google_identity_uid=user.google_identity_uid, email=user.email)

    def to_orm(self) -> User:
        return User(google_identity_uid=self.google_identity_uid, email=self.email)
