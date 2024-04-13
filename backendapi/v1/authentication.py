from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
import jwt


class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu1SU1LfVLPHCozMxH2Mo
4lgOEePzNm0tRgeLezV6ffAt0gunVTLw7onLRnrq0/IzW7yWR7QkrmBL7jTKEn5u
+qKhbwKfBstIs+bMY2Zkp18gnTxKLxoS2tFczGkPLPgizskuemMghRniWaoLcyeh
kd3qqGElvW/VDL5AaWTg0nLVkjRo9z+40RQzuVaE8AkAFmxZzow3x+VJYKdjykkJ
0iT9wCS0DRTXu269V264Vf/3jvredZiKRkgwlL9xNAwxXFg0x/XFw005UWVRIkdg
cKWTjpBP2dPwVZ4WWC+9aGVd+Gyn1o0CLelf4rEjGoXbAAEgAqeGUxrcIlbjXfbc
mwIDAQAB
-----END PUBLIC KEY-----"""

        if "Authorization" in request.headers:
            token = request.headers.get("Authorization")
            # extract the token if header contains a prefix (e.g., Bearer)
            token = token.split()[1]

            try:
                decoded = jwt.decode(jwt=token, key=public_key, algorithms=["RS256"])
                username = decoded["user_name"]
                user = User.objects.get(username=username)
                return (user, None)
            except jwt.exceptions.DecodeError:
                raise exceptions.AuthenticationFailed("Failed to validate token")

        return None

    def authenticate_header(self, request):
        return "Bearer"
