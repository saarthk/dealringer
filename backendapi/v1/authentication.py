from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions
import jwt


# Custom authentication class to authenticate users using JWT

# As per DRF documentation, the typical flow of authentication is as follows:
# 1. If authentication is not attempted, return None. Any other authentication schemes also in use will still be checked.
# 2. If authentication is attempted and fails, raise an AuthenticationFailed exception. An error response will be returned immediately,
# regardless of any permissions checks, and without checking any other authentication schemes.


class CustomJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # A third party user management and authentication service signs
        # the JWT token using the RSA256 private key.

        # RSA256 public key to verify the JWT token.
        # This key can be obtained via an API endpoint of the third party service in a JWKS format.
        # For example, in Clerk, the public key can be obtained from the following endpoint: https://<YOUR_FRONTEND_API>/.well-known/jwks.json
        public_key = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu1SU1LfVLPHCozMxH2Mo
4lgOEePzNm0tRgeLezV6ffAt0gunVTLw7onLRnrq0/IzW7yWR7QkrmBL7jTKEn5u
+qKhbwKfBstIs+bMY2Zkp18gnTxKLxoS2tFczGkPLPgizskuemMghRniWaoLcyeh
kd3qqGElvW/VDL5AaWTg0nLVkjRo9z+40RQzuVaE8AkAFmxZzow3x+VJYKdjykkJ
0iT9wCS0DRTXu269V264Vf/3jvredZiKRkgwlL9xNAwxXFg0x/XFw005UWVRIkdg
cKWTjpBP2dPwVZ4WWC+9aGVd+Gyn1o0CLelf4rEjGoXbAAEgAqeGUxrcIlbjXfbc
mwIDAQAB
-----END PUBLIC KEY-----"""

        # If the user is logged in, the JWT token is sent in the Authorization header.
        if "Authorization" in request.headers:
            # Extract the token string from the header
            token = request.headers.get("Authorization")
            # Extract the token if header contains a prefix (e.g., Bearer)
            token = token.split()[1]

            try:
                decoded = jwt.decode(jwt=token, key=public_key, algorithms=["RS256"])
                # TODO: Check if the token is expired
                username = decoded["user_name"]
                user = User.objects.get(username=username)

                # As per DRF documentation, the `authenticate` method should return a tuple of (user, auth) on success.
                return (user, None)

            # If the token is invalid, raise an AuthenticationFailed exception.
            # The token may be forged or tampered with. As a result, authenication fails and no other authentication schemes will be checked.
            except jwt.exceptions.DecodeError:
                raise exceptions.AuthenticationFailed("Failed to validate token")

        # If the Authorization header is not present, return None to indicate that the authentication process should continue via other schemes
        # specified in the REST_FRAMEWORK setting in settings.py
        return None

    # This method returns a string that will be used as the value of the WWW-Authenticate header in a HTTP 401 Unauthorized response.
    # Refer https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication for more details
    def authenticate_header(self, request):
        return "Bearer"
