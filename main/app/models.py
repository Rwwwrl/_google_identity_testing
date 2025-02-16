from django.db import models


class User(models.Model):
    google_identity_uid: str = models.CharField(max_length=100, unique=True, db_index=True)
    email: str = models.EmailField()


def create_new_user(google_identity_uid: str, email: str) -> User:
    return User.objects.create(google_identity_uid=google_identity_uid, email=email)


def get_user_by_google_identity_uid(google_identity_uid: str) -> User:
    return User.objects.get(google_identity_uid=google_identity_uid)
