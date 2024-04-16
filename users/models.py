from datetime import date
from django.db import models
import uuid
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from users.manager import UserManager
from bubblebackend import settings
from django.db.models import Avg


# --------------  User Auth Model  --------------


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Details
    email = models.EmailField(unique=True, null=False, blank=False)

    username = models.CharField(max_length=100, null=True, blank=True)

    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    phone_number = PhoneNumberField(blank=True, null=True)

    # Roles
  
    is_seller  = models.BooleanField(default=False)

    # Verification
    is_verified = models.BooleanField(default=False)

    # DateTime
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]

        if self.is_superuser:
            self.is_verified = True
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.email


# --------------  Base Profile and Profiles  --------------

class BaseUserProfile(models.Model):
    '''
    A profile to contain a user's(non-organisation) personal info
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Further info
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    display_name = models.CharField(max_length=150, null=True, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='users/profile_pictures', blank=True, null=True)

    address = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        if self.first_name and self.last_name:
            return self.get_fullname()
        return self.user.email

    def get_fullname(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        '''
        Sets user profile ID to the same as the user ID
        '''
        self.id = self.user.id
        super().save(*args, **kwargs)

    def get_object(self):
        return f"{self}"



# --------------  Password Reset Requests  --------------

# class PasswordResetReq(models.Model):
#     token = models.UUIDField(default=uuid.uuid4, editable=False)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_token')
#     active_count = models.IntegerField(default=0)
    
#     # Timestamp
#     created_at = models.DateTimeField(auto_now_add=True)

