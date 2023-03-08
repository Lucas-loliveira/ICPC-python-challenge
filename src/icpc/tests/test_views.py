import pytest
from django.urls import reverse
from rest_framework import status
from icpc.models import Participant, Team, Competition
from icpc.constants import MAX_MEMBERS_PER_TEAM, MAX_SCORE, SCORE_NEEDED_TO_PASS


@pytest.mark.django_db(transaction=True)
def test_create_participant(api_client):
    url = reverse("participant-list")
    data = {
        "first_name": "Lucas",
        "last_name": "Silva",
        "id_number": "123456789",
        "gender": "M",
        "date_of_birth": "2000-01-01",
        "country_of_origin": "Brazil",
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True)
def test_update_participant(api_client, participant):
    url = reverse("participant-detail", args=[participant.id])
    data = {
        "first_name": "Jane",
        "last_name": "Silva",
        "id_number": "987654321",
        "gender": "F",
        "date_of_birth": "2001-01-01",
        "country_of_origin": "Canada",
    }
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["first_name"] == data["first_name"]
    assert response.data["last_name"] == data["last_name"]
    assert response.data["id_number"] == data["id_number"]
    assert response.data["gender"] == data["gender"]
    assert response.data["date_of_birth"] == data["date_of_birth"]
    assert response.data["country_of_origin"] == data["country_of_origin"]


@pytest.mark.django_db(transaction=True)
def test_delete_participant(api_client, participant):
    url = reverse("participant-detail", args=[participant.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Participant.objects.filter(id=participant.id).exists()


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("participants", [MAX_MEMBERS_PER_TEAM], indirect=True)
def test_create_team(api_client, participants):
    participants_ids_list = list(Participant.objects.values_list("id", flat=True))
    url = reverse("team-list")
    data = {"members_id": participants_ids_list}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert (
        Team.objects.get(id=response.json()["id"]).members.count()
        == MAX_MEMBERS_PER_TEAM
    )


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("participants", [MAX_MEMBERS_PER_TEAM + 1], indirect=True)
def test_create_team_exceeded_maximum_members(api_client, participants):
    participants_ids_list = list(Participant.objects.values_list("id", flat=True))
    url = reverse("team-list")
    data = {"members_id": participants_ids_list}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("participants", [MAX_MEMBERS_PER_TEAM], indirect=True)
def test_create_participant_with_diferent_nacionality(api_client, participants):
    participants_ids_list = list(Participant.objects.values_list("id", flat=True))
    foreign_participant = Participant.objects.get(id=participants_ids_list[0])
    foreign_participant.country_of_origin = "Tunisia"
    foreign_participant.save()

    url = reverse("team-list")
    data = {"members_id": participants_ids_list}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert foreign_participant.country_of_origin == "Tunisia"


@pytest.mark.django_db(transaction=True)
def test_create_team_participant_not_exists(api_client):
    url = reverse("team-list")
    data = {"members_id": [1, 2, 3]}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("participants", [1], indirect=True)
def test_update_add_participant(api_client, participants):
    participant = Participant.objects.first()
    team = Team.objects.create()
    url = reverse("team-detail", kwargs={"pk": team.id})
    data = {"members_id": [participant.id]}

    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert Team.objects.get(id=response.json()["id"]).members.count() == 1


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize("participants", [1], indirect=True)
def test_update_remove_participant(api_client, participants):
    participant = Participant.objects.all()
    team = Team.objects.create()
    team.members.set(participant)

    url = reverse("team-detail", kwargs={"pk": team.id})
    data = {"members_id": []}
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert Team.objects.get(id=response.json()["id"]).members.count() == 0


@pytest.mark.django_db(transaction=True)
def test_create_competition(api_client, team):
    url = reverse("competition-list")
    data = {
        "team": team.id,
        "instance": "Local",
        "year": 2019,
        "score": MAX_SCORE,
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["team"] == data["team"]
    assert response.data["instance"] == data["instance"]
    assert response.data["year"] == data["year"]
    assert response.data["score"] == data["score"]


@pytest.mark.django_db(transaction=True)
def test_create_competition_score_out_of_range(api_client, team):
    url = reverse("competition-list")
    data = {
        "team": team.id,
        "instance": "Local",
        "year": 2019,
        "score": MAX_SCORE + 1,
    }
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True)
def test_create_competition_with_no_requirement(api_client, team):
    url = reverse("competition-list")
    data = {
        "team": team.id,
        "instance": "International",
        "year": 2019,
        "score": MAX_SCORE,
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True)
def test_create_competition_with_no_minimun_score(api_client, team):
    url = reverse("competition-list")
    data = {
        "team": team.id,
        "instance": "Local",
        "year": 2019,
        "score": SCORE_NEEDED_TO_PASS - 1,
    }
    response_setup = api_client.post(url, data)

    data = {
        "team": team.id,
        "instance": "National",
        "year": 2019,
        "score": MAX_SCORE,
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
