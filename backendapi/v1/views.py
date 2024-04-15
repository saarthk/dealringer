from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Phone
from .serializers import PhoneSerializer
from svix import Webhook, WebhookVerificationError
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
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
    # permission_classes = [IsAuthenticated]


WEBHOOK_SECRET = "whsec_TJKxLPfHgdrovw42U+YibmFmffo3YK+Q"

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

    logger.info(f"Received webhook: {msg}")

    return Response(status=204)
