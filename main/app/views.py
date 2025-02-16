from django.conf import settings
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from app.dependencies import (
    get_user_google_identity_uid_from_id_token,
    id_token_from_headers,
    verify_id_token,
)
from app.models import create_new_user, get_user_by_google_identity_uid
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


class CreateNewUserFallback(APIView):
    def post(self, request):
        payload = CreateNewUserPayload(**request.data)

        create_new_user(google_identity_uid=payload.user_uid, email=payload.user_email)

        return Response(status=status.HTTP_200_OK)


class UserDetails(APIView):
    def get(self, request):
        id_token = id_token_from_headers(headers=dict(request.headers))
        id_token = verify_id_token(id_token=id_token)

        user_google_identity_uid = get_user_google_identity_uid_from_id_token(id_token=id_token)

        user = get_user_by_google_identity_uid(google_identity_uid=user_google_identity_uid)

        return Response(data=UserSchema.from_orm(user=user).model_dump_json(), status=status.HTTP_200_OK)
