from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import (
    BaseUserProfile, 
    User, 
    # PasswordResetReq
)
from users.serializers import (
    BaseUserProfileSerializer, 
    ChangePasswordSerializer, 
    # ConfirmEmailSerializer, 
    UserInfoSerializer, 
    UserRegistrationSerializer, 
    UserSerializer
)
import uuid
from drf_yasg.utils import swagger_auto_schema
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# -------------- USER VIEWS --------------

class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_class = permissions.IsAuthenticated
    lookup_field = 'pk'
    search_fields = ["first_name", "last_name", "username"]

    # Define a get_serializer_class method that uses a different serializer for user creation
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        if self.action == 'retrieve':
            return UserInfoSerializer
        return super().get_serializer_class()

    # Define a get_permissions method that sets custom permissions based on the action
    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        if self.action == 'list':
            return [permissions.IsAdminUser()]
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        if self.action == 'patch':
            return [permissions.IsAuthenticated()]
        if self.action == 'destroy':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        
        return super().get_permissions()

# -------------- USER PROFILE --------------

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    '''
    Allows user retrieve and update their user profile
    '''
    serializer_class = BaseUserProfileSerializer #permissions.IsAuthenticated, custom_permissions.IsOwnerOrReadOnly
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ["first_name", "last_name", "user__username"]


    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            # A queryset defined for schema generation metadata
            return BaseUserProfile.objects.none()


    def get_object(self):
        if getattr(self, 'swagger_fake_view', False):
            # A queryset defined for schema generation metadata
            return BaseUserProfile.objects.none()
        pk = self.kwargs["pk"]
        #TODO Loop through all profile types and build a dict of profile type and values
        obj = get_object_or_404(BaseUserProfile, id=pk)
       
        self.check_object_permissions(self.request, obj)
        return obj
    

    # def patch(self, request, *args, **kwargs):

    #     return super().patch(request, *args, **kwargs)

   

# -------------- CHANGE & FORGOT PASSWORD --------------
    
# class ChangePasswordView(generics.UpdateAPIView):
#     '''
#     Accepts an old_password and a new password as strings, checks if the hashed
#     old_pssword matches the user's old password and if it does changes the user's
#     password to new_password 
#     '''
#     queryset = get_user_model().objects.all()
#     serializer_class = ChangePasswordSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     # TODO: Add IsObjectOwner permission 

#     @swagger_auto_schema(
#         request_body=ChangePasswordSerializer,
#         responses={status.HTTP_201_CREATED: 'Created',
#                    status.HTTP_400_BAD_REQUEST: 'Bad Request'},
#     )

#     def patch(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         old_password = request.data.get("old_password")
#         if not request.user.check_password(old_password):
#             return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
        
#         new_password = request.data.get("new_password")
#         request.user.set_password(new_password)
#         request.user.save()
        
#         return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
    
