from firebase_admin import auth
from firebase_admin.auth import ExpiredIdTokenError, InvalidIdTokenError


class ValidationFailedException(Exception):
    pass


def verify_id_token(id_token: str) -> str:
    try:
        id_token = auth.verify_id_token(id_token=id_token)
    except (InvalidIdTokenError, ExpiredIdTokenError):
        raise ValidationFailedException

    return id_token


def id_token_from_headers(headers: dict) -> str:
    # example: { Authorization: Bearer <JWT_TOKEN> }
    return headers["Authorization"].split(" ")[-1]


def get_user_google_identity_uid_from_id_token(id_token: str) -> str:
    return id_token["sub"]
