from django.urls import path
from .views import (
    UserViewSet,
    UserProfileDetailView, 

)
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()

# List & Retrieves
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    # Confirm User Info

    # JWT Auth
    path('users/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Change & Reset Password
    # Profiles
    path('users/user-profile/<str:pk>/', UserProfileDetailView.as_view(),  name='user-profile-detail'),

    # Build context for sign-in
    # how to trigger post update signal  
    # Permission to allow only owner of object retrieve it



 
] + router.urls