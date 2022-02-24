from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .models import FulfillmentLevel
from .serializers import FulfillmentLevelSerializer


class Index(APIView):
    def get(self, request):
        endpoints = {
            'levels': '/levels',
            'habits': '/habits/<int:pk>',
        }
        return Response(endpoints)


class FulfillmentLevels(ListAPIView):
    queryset = FulfillmentLevel.objects.all()
    serializer_class = FulfillmentLevelSerializer