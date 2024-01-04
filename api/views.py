
from django.http import HttpResponse
from rest_framework import generics
from .models import Deal, Project, DealProject
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import DealSerializer, ProjectSerializer
import pdb



@api_view(['POST'])
def Createproject(request):
    serializer = ProjectSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def GetDealDetails(request, deal_id=None):
  if deal_id:
    deal = Deal.objects.get(id=deal_id)
    serializer = DealSerializer(deal)
  return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def CreateDeal(request):
#   pdb.set_trace()
  deal_serializer = DealSerializer(data=request.data)

  if deal_serializer.is_valid():
      deal = deal_serializer.save()
  else:
      return Response({'errors': deal_serializer.errors, 'message': 'Errors in deal data'}, status=status.HTTP_400_BAD_REQUEST)
  return Response(deal_serializer.data, status=status.HTTP_201_CREATED)