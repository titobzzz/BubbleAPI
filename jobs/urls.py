from django.urls import path
from .views import *



urlpatterns = [
    path('jobs/', JobsViewSet.as_view({"get":"list", "post":"create"}),name="Create_list_jobs"),
    path('jobs/<str:pk>/', JobsViewSet.as_view({"get":"retrieve", "delete":"destroy"}), name="retieve_update_jobs"),
    path('jobs/<job_id>/apply/', JobProposalViewSet.as_view({"get":"list", "post":"create"}),name="Create_list_jobapps"),
    path('jobs/<job_id>/apply/<str:pk>/', JobProposalViewSet.as_view({"get":"retrieve", "delete":"destroy"}),  name="retieve_update_jobsapps")
]
