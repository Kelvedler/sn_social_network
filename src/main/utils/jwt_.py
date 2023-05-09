import jwt
from typing import Set

from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import authentication, HTTP_HEADER_ENCODING, exceptions, status
from rest_framework.request import Request

from main.utils.time import get_now
from person.models import Person

AUTH_HEADER_TYPES = ('Bearer',)
AUTH_HEADER_NAME = 'HTTP_AUTHORIZATION'
ALGORITHM = 'HS256'
TYPE_ACCESS = 'access'
TYPE_REFRESH = 'refresh'

AUTH_HEADER_TYPE_BYTES: Set[bytes] = {
    h.encode(HTTP_HEADER_ENCODING) for h in AUTH_HEADER_TYPES
}


def encode(identifier, type_, expiration_delta):
    payload = {
        'id': str(identifier),
        'type': type_,
        'exp': timezone.now() + expiration_delta
    }
    return jwt.encode(payload, settings.JWT['SECRET'], algorithm=ALGORITHM)


def encode_access(identifier):
    return encode(identifier, TYPE_ACCESS, settings.JWT['ACCESS_EXPIRATION_DELTA'])


def encode_refresh(identifier):
    return encode(identifier, TYPE_REFRESH, settings.JWT['REFRESH_EXPIRATION_DELTA'])


class InvalidToken(exceptions.AuthenticationFailed):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _("Token is invalid or expired")
    default_code = "token_not_valid"


class JWTAuthentication(authentication.BaseAuthentication):
    www_authenticate_realm = "api"
    media_type = "application/json"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user_model = Person

    def authenticate(self, request: Request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        person = self.get_person(validated_token)
        person.is_anonymous = False
        person.is_authenticated = True

        return person, validated_token

    def authenticate_header(self, request):
        return '{} realm="{}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    @staticmethod
    def get_header(request):
        header = request.META.get(AUTH_HEADER_NAME)

        if isinstance(header, str):
            header = header.encode(HTTP_HEADER_ENCODING)

        return header

    @staticmethod
    def get_raw_token(header):
        parts = header.split()

        if len(parts) == 0:
            # Empty AUTHORIZATION header sent
            return None

        if parts[0] not in AUTH_HEADER_TYPE_BYTES:
            # Assume the header does not contain a JSON web token
            return None

        if len(parts) != 2:
            raise exceptions.AuthenticationFailed()

        return parts[1]

    @staticmethod
    def get_validated_token(raw_token):
        try:
            payload = jwt.decode(raw_token, settings.SECRET_KEY, ALGORITHM)
        except (jwt.DecodeError, jwt.InvalidTokenError, jwt.ExpiredSignatureError):
            raise InvalidToken()

        try:
            exp = payload['exp']
            assert exp > get_now().timestamp()
        except (KeyError, AssertionError):
            raise InvalidToken()
        return payload

    @staticmethod
    def get_person(validated_token):
        try:
            person_id = validated_token['id']
        except KeyError:
            raise InvalidToken()

        try:
            person = Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            raise exceptions.AuthenticationFailed()

        person.last_activity = get_now()
        person.save()
        return person
