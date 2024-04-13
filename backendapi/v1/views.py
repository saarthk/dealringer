from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_phone_price(request, model_name):
    response_str = f"{request.user} has requested for the price of {model_name}"
    return Response({"message": response_str})
