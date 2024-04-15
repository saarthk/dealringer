from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Phone
from .serializers import PhoneSerializer


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


