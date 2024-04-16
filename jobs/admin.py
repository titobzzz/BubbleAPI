from django.contrib import admin
from .models import *



class JobAdmin(admin.ModelAdmin):
    search_fields = ['title', 'listed_by__user__email', 'location']
    list_display = ['id', 'title', 'listed_by',
                    'location', 'status', 'role_type']
    list_filter = ['status', 'role_type', 'created_at']
    ordering = ['-created_at']


@admin.register(JobProposals)
class JobProposalsAdmin(admin.ModelAdmin):
    search_fields = ['applicant__first_name', 'applicant__last_name', 'job__title']
    list_filter = ['status', 'created_at']
    list_display = ['id', 'applicant', 'job', 'status', 'created_at']

    ordering = ['-created_at']



# admin.site.register(Job, JobAdmin)
# admin.site.register(JobProposals, JobProposalsAdmin)

