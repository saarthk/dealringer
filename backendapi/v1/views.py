from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Phone, Price
from .serializers import PhoneSerializer, PriceSerializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt
from svix import Webhook, WebhookVerificationError
import logging

logger = logging.getLogger("django")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_phone_price(request, model_name):
    response_str = f"{request.user} has requested for the price of {model_name}"
    return Response({"message": response_str})


# ViewSet to provide read-only access to Phone model
# GET method handlers are provided by default to:
# 1. Retrieve a list of all phones
# 2. Retrieve a single phone by its primary key
class PhoneReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    permission_classes = [IsAuthenticated]

    # Custom action to retrieve all prices of a phone (across all sellers)
    @action(methods=["get"], detail=True, permission_classes=[IsAuthenticated])
    def prices(self, request, pk=None):
        # self.get_object() returns the phone instance corresponding to the primary key (pk)
        # Refer https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
        phone = self.get_object()
        prices = phone.prices.all()
        serializer = PriceSerializer(prices, many=True)
        return Response(serializer.data)


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    permission_classes = [IsAuthenticated]


def get_primary_email_address(email_addresses, primary_email_address_id):
    for email in email_addresses:
        if email["id"] == primary_email_address_id:
            return email["email_address"]
    return None


WEBHOOK_SECRET = "whsec_P0xBIyOtYsTOyxDJ/u4ixfM0Tt8iRnW6"


# Webhook view to receive and verify webhooks.
# The third-party user management service sends a POST request to this endpoint when:
# 1. A user is created
# 2. A user is updated
# 3. A user is deleted
# The webhook payload contains the user details and the event type.
@csrf_exempt
@api_view(["POST"])
def webhook_view(request):
    headers = request.headers
    payload = request.body

    try:
        wh = Webhook(WEBHOOK_SECRET)
        # Verify the webhook payload and headers using the secret
        msg = wh.verify(payload, headers)
    except WebhookVerificationError as e:
        return Response({"error": str(e)}, status=400)

    msg_data = msg["data"]

    # Handle user CREATE event
    if msg["type"] == "user.created":
        # Extract user details from the webhook payload
        # Assign default username as "AnonymousUser" if username is not provided
        username = msg_data["username"] or "AnonymousUser"
        # Extract primary email address from the list of email addresses
        email_address = get_primary_email_address(
            msg_data["email_addresses"], msg_data["primary_email_address_id"]
        )
        first_name = msg_data["first_name"]
        last_name = msg_data["last_name"]
        userid = msg_data["id"]

        user_data = {
            "username": username,
            "email": email_address,
            "first_name": first_name,
            "last_name": last_name,
            "additional_info": {"userid_3p": userid},
        }

        # Create a UserSerializer instance and validate the user data
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            # Save the user data to the database (if valid)
            user_serializer.save()
            logger.info(f"User created: {username}")
            return Response(status=204)
        else:
            logger.error(f"User creation failed: {user_serializer.errors}")
            return Response(user_serializer.errors, status=400)

    # Handle user DELETE event
    elif msg["type"] == "user.deleted":
        userid = msg_data["id"]

        try:
            # Get user whose third-party user ID matches the user ID in the webhook payload
            user = User.objects.get(additional_info__userid_3p=userid)
            # Delete the user
            user.delete()
            logger.info(f"User deleted: {user.get_username()}")
            return Response(status=204)
        # If user does not exist, return 404
        except User.DoesNotExist:
            logger.error(f"User not found with userid: {userid}")
            return Response({"error": "User not found"}, status=404)
