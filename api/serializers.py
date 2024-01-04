
from rest_framework import serializers
from .models import Deal, Project, DealProject
# import pdb

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
    tax_credit_transfer_amount = serializers.SerializerMethodField()


    class Meta:
        model = Deal
        fields = ['id', 'name', 'projects', 'tax_credit_transfer_amount']

    def get_tax_credit_transfer_amount(self, instance):
        total_amount = 0
        for deal_project in instance.dealproject_set.all():
            fmv = float(deal_project.project.fmv)
            tax_credit_transfer_rate = float(deal_project.tax_credit_transfer_rate)
            total_amount += fmv * 0.3 * tax_credit_transfer_rate
        return total_amount

    def create(self, validated_data):
        dealprojects_data = validated_data.pop('dealproject_set', [])
        deal = Deal.objects.create(**validated_data)

        for dealproject_data in dealprojects_data:
            project_data = dealproject_data.pop('project', {})
            project_serializer = ProjectSerializer(data=project_data)
            # pdb.set_trace()

            if project_serializer.is_valid():
                project = project_serializer.save()
                DealProject.objects.create(deal=deal,project=project,tax_credit_transfer_rate=dealproject_data.get('tax_credit_transfer_rate'))
            else:
                # Handle validation errors for projects if needed
                pass

        return deal
        
