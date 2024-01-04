
from rest_framework import serializers
from .models import Deal, Project, DealProject

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'fmv']

class DealProjectSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = DealProject
        fields = ['id', 'project', 'tax_credit_transfer_rate']

class DealSerializer(serializers.ModelSerializer):
    projects = DealProjectSerializer(many=True, source='dealproject_set')

    class Meta:
        model = Deal
        fields = ['id', 'name', 'projects']

    def create(self, validated_data):
        projects_data = validated_data.pop('projects', [])
        deal = Deal.objects.create(**validated_data)
        for project_data in projects_data:
            project_serializer = ProjectSerializer(data=project_data['project'])
            if project_serializer.is_valid():
                project = project_serializer.save()
                DealProject.objects.create(deal=deal, project=project, tax_credit_transfer_rate=project_data['tax_credit_transfer_rate'])
            else:
                # Handle validation errors for projects if needed
                pass
        return deal
