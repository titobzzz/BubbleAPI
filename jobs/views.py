from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
import os
from django.shortcuts import get_object_or_404
from django.db.models import Q
from drf_yasg import openapi
from django.core.mail import send_mail
from django.conf import settings
from users.models import User
from jobs.models import *
from jobs.serializers import *
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


class JobsViewSet(viewsets.ModelViewSet):

    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permissions_classes = []
 

    def get_permission(self, request):
        if request.method in ["POST","GET"]:
            return []
        elif request.method in ["UPDDATE", "DELETE" ]:
            job = Job.objects.get(id = request.kwargs("pk"))
            if request.user == job.listed_by:
                return [IsAuthenticated]
            else:
                return Response("Only creators can update or delete Jobs")
        


class JobProposalViewSet(viewsets.ModelViewSet):

    queryset =  JobProposals.objects.all()
    serializer_class = JobProposalSerializer
    permissions_classes = []
 

    def get_permission(self, request):
        proposal = JobProposalSerializer.objects.get(id = request.kwargs("pk"))
        if request.method == ["POST"]:
            if request.user.is_seller == False:
                 return Response("Please create seller account and try again")
            else:
                return []
        elif request.method in [ "DELETE" ]:           
            if request.user == proposal.applicant:
                return [IsAuthenticated]
            else:
                return Response("Only creators can delete Jobs")
        elif request.method in ["UPDATE", "PATCH"]:
            job = Job.objects.get(id = request.kwargs("job_id"))
            if request.user == job.listed_by:
                return [IsAuthenticated]
            elif request.user == proposal.applicant:
                 return [IsAuthenticated]
            return Response("Only creators can update Jobs")
        
        
    def get_serializer_class(self, request, *args, **kwargs ):
        if request.method in ["POST","GET","DELETE"]:
            return super.get_serializer_class()
        elif request.method in ["UPDATE", "PATCH"]:

            return  JobProposalsStatusSerializer

            


            

        

