from django.contrib.auth.password_validation import validate_password
from django.forms import ValidationError
from rest_framework import serializers
from .models import BaseUserProfile, User
from django.contrib.auth.hashers import check_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    # print('Create user srlzr')
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'email', "first_name", "last_name", 'password']

    # Validates email entered by user
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email address already exists.")
        return value

    # Validates password entered by user
    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    # Creates a new user object using validated data
    def create(self, validated_data):

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],

            is_verified=False

        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'email', 'is_student',
        #           'is_instructor', 'is_hirer', 'is_job_hunting', 'is_organisation']
        # fields = '__all__'
        exclude = ['password']


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class BaseUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BaseUserProfile
        #fields = "__all__"
        exclude = ['user']



# ------------- CHANGE & RESET PASSWORD -------------

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    def validate_new_password(self, value):
        # Validate the password meets strength requirements
        validate_password(value)
        return value

    def validate_old_password(self, value):
        user = self.context['request'].user
        # Check if the old password matches the current password of the user
        if not check_password(value, user.password):
            raise serializers.ValidationError("Old password does not match.")
        return value
    
    def validate(self, data):
        old_password = data.get('old_password', None)
        new_password = data.get('new_password', None)

        if old_password == new_password:
            raise serializers.ValidationError("New password cannot be the same as old password.")

        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


    # def validate_email(self):
    #     pass



class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        # Validate the password meets strength requirements
        validate_password(value)
        return value
    

class ConfirmEmailSerializer(serializers.ModelSerializer):
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        model = User
        fields = ['token', 'uidb64']