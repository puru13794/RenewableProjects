
from django.http import HttpResponse
from rest_framework import generics
from .models import Deal, Project, DealProject
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import DealSerializer, ProjectSerializer


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
  deal_serializer = DealSerializer(data=request.data.get('deal'))

  if deal_serializer.is_valid():
      deal = deal_serializer.save()
  else:
      return Response({'errors': deal_serializer.errors, 'message': 'Errors in deal data'}, status=status.HTTP_400_BAD_REQUEST)
  projects_data = request.data.get('projects', [])

  #collect error in project data if any?
  project_errors = []
  for project_data in projects_data:
      #check if project exists
      project_id = project_data.get('id')
      if project_id:
        try:
            project = Project.objects.get(id=project_id)
            project_serializer = ProjectSerializer(instance=project, data=project_data, partial=True)
        except Project.DoesNotExist:
            project_serializer = ProjectSerializer(data=project_data)
        else:
            project_serializer = ProjectSerializer(data=project_data)
      
      if project_serializer.is_valid():
        project = project_serializer.save()
        DealProject.objects.create(
          deal=deal,
          project=project,
          tax_credit_transfer_rate=project_data.get('tax_credit_transfer_rate')
        )
      else:
        # project_errors.appened('Incorrect Project data passed' + project_serializer.errors)
        for err in project_serializer.errors:
            project_errors.appened(err)
  if not project_errors:
    return Response(deal_serializer.data, status=status.HTTP_201_CREATED)
  return Response(project_errors, status=status.HTTP_400_BAD_REQUEST)