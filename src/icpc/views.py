from rest_framework import generics
from .serializers import ParticipantSerializer, TeamSerializer, CompetitionSerializer
from .models import Participant, Team, Competition
from rest_framework.exceptions import NotFound


class ParticipantList(generics.ListCreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class ParticipantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer


class TeamList(generics.ListCreateAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class CompetitionList(generics.ListCreateAPIView):
    serializer_class = CompetitionSerializer

    def get_queryset(self):
        queryset = Competition.objects.all().order_by("year", "instance", "-score")
        year = self.request.query_params.get("year")
        instance = self.request.query_params.get("instance")

        filter = {}
        if year:
            filter["year"] = year
        if instance:
            instance_db = [
                v[0] for v in Competition.instance.field.choices if v[1] == instance
            ]
            if not instance_db:
                raise NotFound("Instance not valid")
            filter["instance"] = instance_db[0]

        if filter:
            queryset = queryset.filter(**filter).order_by("year", "instance", "-score")
        return queryset


class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
