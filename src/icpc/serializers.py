from rest_framework import serializers
from .models import Participant, Team, Competition
from .constants import (
    MAX_MEMBERS_PER_TEAM,
    COMPETITION_REQUIREMENT,
    MAX_SCORE,
    MIN_SCORE,
    SCORE_NEEDED_TO_PASS,
)


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    members = ParticipantSerializer(many=True, read_only=True)
    members_id = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, allow_empty=True, default=[]
    )

    class Meta:
        model = Team
        fields = "__all__"
        extra_kwargs = {"members_id": {"write_only": True}}

    def validate(self, data):
        team_members_ids = data.get("members_id", [])
        if len(team_members_ids) > MAX_MEMBERS_PER_TEAM:
            raise serializers.ValidationError(
                "Maximum number of members per team exceeded"
            )
        return data

    def create(self, validated_data):
        team_members_ids = validated_data.pop("members_id")

        participants = self.get_participants_by_id(team_members_ids)

        if not self.check_members_same_country(participants):
            raise serializers.ValidationError(
                "Participants are not from the same country"
            )

        team_instance = Team.objects.create(**validated_data)
        team_instance.members.set(participants)
        team_instance.save()
        return team_instance

    def update(self, instance, validated_data):
        team_members_ids = validated_data.pop("members_id")
        participants = self.get_participants_by_id(team_members_ids)

        if not self.check_members_same_country(participants):
            raise serializers.ValidationError(
                "Participants are not from the same country"
            )
        instance.members.set(participants)

        return instance

    def check_members_same_country(self, participants: Participant) -> bool:
        if not participants:
            return True
        countrys_of_origin = [
            participant.country_of_origin for participant in participants
        ]

        return True if len(set(countrys_of_origin)) == 1 else False

    def get_participants_by_id(self, participants_id):
        participants = Participant.objects.filter(id__in=participants_id)
        if participants.count() != len(participants_id):
            raise serializers.ValidationError("Participants not found")
        return participants


class ChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == "" and self.allow_blank:
            return obj
        return self._choices[obj]

    def to_internal_value(self, data):
        if data == "" and self.allow_blank:
            return ""

        for key, val in self._choices.items():
            if val == data:
                return key
        self.fail("invalid_choice", input=data)


class CompetitionSerializer(serializers.ModelSerializer):
    team = TeamSerializer()
    instance = ChoiceField(choices=Competition.INSTANCE_CHOICE)

    class Meta:
        model = Competition
        fields = "__all__"

    def to_internal_value(self, data):
        self.fields["team"] = serializers.PrimaryKeyRelatedField(
            queryset=Team.objects.all()
        )
        return super(CompetitionSerializer, self).to_internal_value(data)

    def validate(self, data):
        score = data.get("score")
        if not (MIN_SCORE <= score <= MAX_SCORE):
            raise serializers.ValidationError("Score out of range")

        competition_requirement = COMPETITION_REQUIREMENT.get(
            data.get("instance", None)
        )
        if competition_requirement:
            last_competition = Competition.objects.filter(
                team=data.get("team"),
                year=data.get("year"),
                instance=competition_requirement,
            )
            
            if not last_competition:
                raise serializers.ValidationError(
                    f"The team needs results in the {competition_requirement} competition"
                )
            if last_competition[0].score < SCORE_NEEDED_TO_PASS:
                raise serializers.ValidationError(
                    f"The team needs a minimum score of {SCORE_NEEDED_TO_PASS} in phase {competition_requirement} to advance"
                )

        return data
