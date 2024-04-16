from rest_framework import serializers
from .models import *
from users.models import BaseUserProfile
from users.serializers import BaseUserProfileSerializer




class JobSerializer(serializers.ModelSerializer):
    liked_by = BaseUserProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = [
            'id',
            'listed_by',
            'title',
            'description',
            'location',
            'fixed_payment',
            'pay',
            'pay_currency',
            'status',
            'role_type',
            'created_at',
            'updated_at',
        ]


class JobProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProposals
        fields = '__all__'
        read_only_fields = [
            "status"
        ]

class JobProposalsStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProposals
        fields = 'status'
