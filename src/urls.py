from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from icpc.views import ParticipantList,ParticipantDetail,TeamDetail,TeamList,CompetitionDetail,CompetitionList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('participant/', ParticipantList.as_view(), name = "participant-list"),
    path('participant/<int:pk>/', ParticipantDetail.as_view(), name="participant-detail"),
    path('team/', TeamList.as_view(), name = "team-list"),
    path('team/<int:pk>/', TeamDetail.as_view(), name="team-detail"),
    path('competition/', CompetitionList.as_view(), name = "competition-list"),
    path('competition/<int:pk>/', CompetitionDetail.as_view(), name="competition-detail"),
]


