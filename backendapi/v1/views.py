from typing import override
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Phone, Posting
from .serializers import PhoneSerializer, PostingSerializer, UserSerializer
from django.views.decorators.csrf import csrf_exempt
from svix import Webhook, WebhookVerificationError
import logging
from django.contrib.postgres.search import SearchVector, SearchQuery

logger = logging.getLogger("django")


class SearchPhones(ListAPIView):
    serializer_class = PhoneSerializer
    permission_classes = [AllowAny]

    @override
    def get_queryset(self):
        # Extract the query parameter from the request
        query = self.request.query_params.get("q")

        if query is not None and query != "":
            # Perform full-text search on the brand_name and model_name fields
            query = SearchQuery(query)
            return Phone.objects.annotate(
                search=SearchVector("brand_name", "model_name")
            ).filter(search=query)
        return Phone.objects.all()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_saved_phones(request):
    user = request.user
    saved_phones = user.additional_info.saved_phones.all()
    serializer = PhoneSerializer(saved_phones, many=True)
    return Response(serializer.data)


# ViewSet to provide read-only access to Phone model
# This viewset is not authenticated (permission class is AllowAny),
# since it does not expose any sensitive information, and is intended to be used by anyone.


# GET method handlers are provided by default to:
# 1. Retrieve a list of all phones
# 2. Retrieve a single phone by its primary key
class PhoneReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer
    permission_classes = [AllowAny]

    # Retrieve all postings of a phone (across all sellers).
    @action(methods=["get"], detail=True)
    def postings(self, request, pk=None):
        # self.get_object() returns the phone instance corresponding to the primary key (pk)
        # Refer https://www.django-rest-framework.org/api-guide/generic-views/#genericapiview
        phone = self.get_object()
        postings = phone.postings.all()
        serializer = PostingSerializer(postings, many=True)
        return Response(serializer.data)

    # Retrieve the minimum price for a phone
    # @action(methods=["get"], detail=True, url_path="minprice")
    # def minimum_price(self, request, pk=None):
    #     phone = self.get_object()
    #     postings = phone.postings.all()
    #     min_price = postings.aggregate(Min("price"))
    #     # aggregate returns a dictionary with <field>__<function> as the key
    #     min_price = min_price["price__min"]
    #     return Response({"phone": phone.id, "min_price": min_price})

    # Adding and removing bookmarks are idempotent actions. Hence, PUT and DELETE methods are used.
    # IMPORTANT: Permissions are set to IsAuthenticated, since only authenticated users can bookmark a phone.
    @action(
        methods=["put", "delete"],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def bookmark(self, request, pk=None):
        phone = self.get_object()
        user = request.user

        # Add phone to bookmarks
        if request.method == "PUT":
            user.additional_info.saved_phones.add(phone)
            return Response(f"{phone.brand_name} {phone.model_name} bookmarked")
        # Remove phone from bookmarks
        elif request.method == "DELETE":
            user.additional_info.saved_phones.remove(phone)
            return Response(
                f"{phone.brand_name} {phone.model_name} removed from bookmarks"
            )


class PostingViewSet(viewsets.ModelViewSet):
    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
    permission_classes = [IsAuthenticated]


def get_primary_email_address(email_addresses, primary_email_address_id):
    for email in email_addresses:
        if email["id"] == primary_email_address_id:
            return email["email_address"]
    return None


WEBHOOK_SECRET = "whsec_MG7lOShy4a13QgWyxFi18CPJcM2SuTk9"


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
