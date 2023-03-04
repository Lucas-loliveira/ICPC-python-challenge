
from rest_framework import serializers
from .models import Participant,Team,Competition



class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    members = ParticipantSerializer(many=True)

    class Meta:
        model = Team
        fields = '__all__'


class CompetitionSerializer(serializers.ModelSerializer):
    team = TeamSerializer()

    class Meta:
        model = Competition
        fields = '__all__'
