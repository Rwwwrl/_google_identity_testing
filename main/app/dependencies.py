import jwt
from firebase_admin import auth, get_app
from firebase_admin.auth import ExpiredIdTokenError, InvalidIdTokenError, RevokedIdTokenError

from app.models import UserPK


class IdTokenValidationFailedException(Exception):
    pass


def verify_id_token(id_token: str) -> str:
    unverified_claims = jwt.decode(id_token, options={"verify_signature": False})
    tenant_id = unverified_claims.get("firebase", {}).get("tenant")

    if tenant_id is None:
        raise IdTokenValidationFailedException("tenant id is not specified")

    tenant_auth_client = auth.Client(app=get_app(), tenant_id=tenant_id)

    try:
        id_token = tenant_auth_client.verify_id_token(id_token=id_token, check_revoked=True)
    except (InvalidIdTokenError, ExpiredIdTokenError, RevokedIdTokenError):
        raise IdTokenValidationFailedException

    return id_token


def id_token_from_headers(headers: dict) -> str:
    # example: { Authorization: Bearer <JWT_TOKEN> }
    return headers["Authorization"].split(" ")[-1]


def get_user_pk_from_token(id_token: str) -> UserPK:
    return UserPK(
        google_identity_uid=id_token["sub"],
        tenant_id=id_token["firebase"]["tenant"],
    )
