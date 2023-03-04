import pytest
from django.urls import reverse
from rest_framework import status
from icpc.models import Participant, Team, Competition

@pytest.mark.django_db(transaction=True)
def test_create_participant(api_client):
    url = reverse('participant-list')
    data = {
        'first_name': 'Lucas',
        'last_name': 'Silva',
        'id_number': '123456789',
        'gender': 'M',
        'date_of_birth': '2000-01-01',
        'country_of_origin': 'Brazil'
    }
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED

@pytest.mark.django_db(transaction=True)
def test_update_participant(api_client, participant):
    url = reverse('participant-detail', args=[participant.id])
    data = {
        'first_name': 'Jane',
        'last_name': 'Silva',
        'id_number': '987654321',
        'gender': 'F',
        'date_of_birth': '2001-01-01',
        'country_of_origin': 'Canada'
    }
    response = api_client.put(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['first_name'] == data['first_name']
    assert response.data['last_name'] == data['last_name']
    assert response.data['id_number'] == data['id_number']
    assert response.data['gender'] == data['gender']
    assert response.data['date_of_birth'] == data['date_of_birth']
    assert response.data['country_of_origin'] == data['country_of_origin']

@pytest.mark.django_db(transaction=True)
def test_delete_participant(api_client, participant):
    url = reverse('participant-detail', args=[participant.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Participant.objects.filter(id=participant.id).exists()
