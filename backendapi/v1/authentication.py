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
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6S7asUuzq5Q/3U9rbs+P
kDVIdjgmtgWreG5qWPsC9xXZKiMV1AiV9LXyqQsAYpCqEDM3XbfmZqGb48yLhb/X
qZaKgSYaC/h2DjM7lgrIQAp9902Rr8fUmLN2ivr5tnLxUUOnMOc2SQtr9dgzTONY
W5Zu3PwyvAWk5D6ueIUhLtYzpcB+etoNdL3Ir2746KIy/VUsDwAM7dhrqSK8U2xF
CGlau4ikOTtvzDownAMHMrfE7q1B6WZQDAQlBmxRQsyKln5DIsKv6xauNsHRgBAK
ctUxZG8M4QJIx3S6Aughd3RZC4Ca5Ae9fd8L8mlNYBCrQhOZ7dS0f4at4arlLcaj
twIDAQAB
-----END PUBLIC KEY-----"""

        # If the user is logged in, the JWT token is sent in the Authorization header.
        if "Authorization" in request.headers:
            # Extract the token string from the header
            token = request.headers.get("Authorization")
            # Extract the token if header contains a prefix (e.g., Bearer)
            token = token.split()[1]

            try:
                decoded = jwt.decode(
                    jwt=token,
                    key=public_key,
                    algorithms=["RS256"],
                    # TODO: Add azp claim to the required claims list, and add verification logic for the claim
                    options={"require": ["exp", "nbf", "sub"]},
                )
                userid = decoded["sub"]

                # Retrieve the user object from the database using the userid
                user = User.objects.get(additional_info__userid_3p=userid)

                # As per DRF documentation, the `authenticate` method should return a tuple of (user, auth) on success.
                return (user, None)

            # Raise an AuthenticationFailed exception if:
            # 1. The token has expired.
            # 2. The token is not yet valid.
            # 3. The token does not contain the required claims.
            # 4. The token is invalid.
            # 5. The user is not found in the database.
            # Authenication fails and no other authentication schemes will be checked.
            except jwt.exceptions.ExpiredSignatureError:
                raise exceptions.AuthenticationFailed("Token has expired")
            except jwt.exceptions.ImmatureSignatureError:
                raise exceptions.AuthenticationFailed("Premature token")
            except jwt.exceptions.MissingRequiredClaimError:
                raise exceptions.AuthenticationFailed(
                    "Missing required claims. The token should contain 'exp', 'nbf', and 'sub' claims."
                )
            except jwt.exceptions.DecodeError:
                raise exceptions.AuthenticationFailed("Failed to validate token")
            except User.DoesNotExist:
                raise exceptions.AuthenticationFailed(f"User {userid} not found")

        # If the Authorization header is not present, return None to indicate that the authentication process should continue via other schemes
        # specified in the REST_FRAMEWORK setting in settings.py
        return None

    # This method returns a string that will be used as the value of the WWW-Authenticate header in a HTTP 401 Unauthorized response.
    # Refer https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication for more details
    def authenticate_header(self, request):
        return "Bearer"
