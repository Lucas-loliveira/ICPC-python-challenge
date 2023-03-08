import pytest
from icpc.models import Participant, Team, Competition
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def participant():
    return Participant.objects.create(
        first_name="Lucas",
        last_name="Silva",
        id_number="123456789",
        gender="M",
        date_of_birth="2000-01-01",
        country_of_origin="Brazil",
    )


@pytest.fixture
def participants(request):
    participants = []
    for i in range(request.param):
        participant = Participant.objects.create(
            first_name=f"Lucas{i+1}",
            last_name="Silva",
            id_number=f"{i+1}234567890",
            gender="M",
            date_of_birth=f"199{i%10}-01-01",
            country_of_origin="USA",
        )
        participants.append(participant)
    return participants


@pytest.fixture
def team(participant):
    participant = Participant.objects.all()
    team = Team.objects.create()
    team.members.set(participant)
    return team
