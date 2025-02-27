from django.conf import settings
from django.shortcuts import render
from django.views import View
from firebase_admin import auth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.dependencies import (
    IdTokenValidationFailedException,
    get_user_pk_from_token,
    id_token_from_headers,
    verify_id_token,
)
from app.models import create_new_user, get_user_by_pk
from app.schemas import CreateNewUserPayload, UserSchema


class LoginPage(View):
    def get(self, request):
        return render(
            request=request,
            template_name="app/login.html",
            context={
                "apiKey": settings.CONFIG.FIREBASE_CONFIG.api_key,
                "authDomain": settings.CONFIG.FIREBASE_CONFIG.auth_domain,
            },
        )


class Logout(APIView):
    def post(self, request):
        id_token = id_token_from_headers(headers=dict(request.headers))
        try:
            id_token = verify_id_token(id_token=id_token)
        except IdTokenValidationFailedException:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_pk = get_user_pk_from_token(id_token=id_token)

        auth.revoke_refresh_tokens(uid=user_pk.google_identity_uid)
        return Response(status=status.HTTP_200_OK)


class UserDelete(APIView):
    def delete(self, request):
        id_token = id_token_from_headers(headers=dict(request.headers))
        try:
            id_token = verify_id_token(id_token=id_token)
        except IdTokenValidationFailedException:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_google_identity_uid = get_user_pk_from_token(id_token=id_token)

        auth.delete_user(uid=user_google_identity_uid)

        return Response(status=status.HTTP_200_OK)


class CreateNewUserFallback(APIView):
    def post(self, request):
        payload = CreateNewUserPayload(**request.data)

        create_new_user(
            google_identity_uid=payload.user_uid,
            email=payload.user_email,
            tenant_id=payload.tenant_id,
        )

        return Response(status=status.HTTP_200_OK)


class UserDetails(APIView):
    def get(self, request):
        id_token = id_token_from_headers(headers=dict(request.headers))
        try:
            id_token = verify_id_token(id_token=id_token)
        except IdTokenValidationFailedException:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        user_pk = get_user_pk_from_token(id_token=id_token)

        user = get_user_by_pk(pk=user_pk)

        return Response(data=UserSchema.from_orm(user=user).model_dump_json(), status=status.HTTP_200_OK)
