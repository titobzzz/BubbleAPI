from django.contrib import admin

from .models import (
    BaseUserProfile,
    User,
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username", "first_name", "last_name")
    list_filter = ["is_superuser"]
    search_fields = ( "email", "username", "first_name", "last_name",)

@admin.register(BaseUserProfile)
class BaseUserProfileAdmin(admin.ModelAdmin):
    list_display  =  ["id", "user","display_name", "gender"]
    list_filter   =  ["gender"]
    search_fields =  ["user", "display_name"]
