import pytest
from icpc.models import Participant, Team, Competition
from rest_framework.test import APIClient



@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def participant():
    return Participant.objects.create(
        first_name='Lucas',
        last_name='Silva',
        id_number='123456789',
        gender='M',
        date_of_birth='2000-01-01',
        country_of_origin='Brazil'
    )

@pytest.fixture
def team(participant):
    return Team.objects.create(
        name='Team A',
        representative=participant,
        country_of_origin='Brazil'
    )

@pytest.fixture
def competition_result(team):
    return Competition.objects.create(
        team=team,
        year=2022,
        instance='Local',
        score=80
    )
