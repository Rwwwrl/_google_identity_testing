from django.db import models

from app.common import DTO


class UserPK(DTO):
    google_identity_uid: str
    tenant_id: str


class User(models.Model):
    google_identity_uid: str = models.CharField(max_length=100, unique=True, db_index=True)
    email: str = models.EmailField()
    tenant_id: str = models.CharField(max_length=255)

    class Meta:
        unique_together = ("google_identity_uid", "tenant_id")


def create_new_user(google_identity_uid: str, email: str, tenant_id: str) -> User:
    return User.objects.create(google_identity_uid=google_identity_uid, email=email, tenant_id=tenant_id)


def get_user_by_pk(pk: User) -> User:
    return User.objects.get(google_identity_uid=pk.google_identity_uid, tenant_id=pk.tenant_id)
