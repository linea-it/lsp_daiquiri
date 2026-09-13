"""Service-to-service authentication for the Canvas <-> Daiquiri TAP integration.

Canvas mints a short-lived HS256 JWT per request (see
canvas/backend/target/metadata/daiquiri_auth.py::mint_service_token) and sends
it as `Authorization: Bearer <token>`. This class only *resolves* an already
existing local user from the token's `sub` claim - it never creates one, since
account provisioning between the two systems is a separate, manual step
(same username required on both sides).
"""

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

SERVICE_JWT_AUDIENCE = "daiquiri-tap"
SERVICE_JWT_ALGORITHM = "HS256"


class ServiceJWTAuthentication(BaseAuthentication):
    """Authenticates requests carrying a Canvas-minted service JWT.

    Returns None (not an exception) when there is no Bearer token, so this
    class can be prepended to the existing authentication_classes tuple
    without breaking Session/Basic/Token auth for every other caller.
    """

    def authenticate(self, request):
        header = request.META.get("HTTP_AUTHORIZATION", "")
        if not header.startswith("Bearer "):
            return None

        token = header[len("Bearer ") :].strip()
        secret = getattr(settings, "CANVAS_SERVICE_JWT_SECRET", None)
        if not secret:
            msg = "CANVAS_SERVICE_JWT_SECRET is not configured."
            raise AuthenticationFailed(msg)

        try:
            claims = jwt.decode(
                token,
                secret,
                algorithms=[SERVICE_JWT_ALGORITHM],
                audience=SERVICE_JWT_AUDIENCE,
            )
        except jwt.PyJWTError as exc:
            msg = "Invalid service token."
            raise AuthenticationFailed(msg) from exc

        username = claims.get("sub")
        if not username:
            msg = "Service token is missing the 'sub' claim."
            raise AuthenticationFailed(msg)

        user_model = get_user_model()
        try:
            user = user_model.objects.get(username=username, is_active=True)
        except user_model.DoesNotExist as exc:
            msg = f"No active local user matching service token subject '{username}'."
            raise AuthenticationFailed(msg) from exc

        return (user, token)
