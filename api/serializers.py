
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
    projects = DealProjectSerializer(many=True)

    class Meta:
        model = Deal
        fields = ['id', 'name', 'projects']
