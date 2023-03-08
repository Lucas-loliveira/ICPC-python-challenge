# ICPC-python-challenge
Author: Lucas da Silva de Oliveira (lucasoliveira783@gmail.com, https://www.linkedin.com/in/lucas-sil-oliveira)

Objective
=================
Create a program that will manage participants, teams and results related to the ACM-ICPC competition (International Collegiate Programming Contest)

Main technologies used:
  * python3
  * django 4.1
  * django-rest framework
  * PostgreSQL
  * pytest
 
Requirements
============
  * [docker](https://www.docker.com/)
  * [docker-compose](https://docs.docker.com/compose/)

How to run the app
============

### Run the containers
```bash
$ make build up
```

### Run the migrations
```bash
$ make migrate
```

Tests
=====

```bash
$ make test
```

cUrls with examples
=====

### POST Participant
```
curl --request POST \
  --url http://localhost:8000/participant/ \
  --header 'Content-Type: application/json' \
  --cookie csrftoken=rXrStS5ouDlC2I2GqL9DnIhjVGnwzdcZ \
  --data '{
    "first_name": "Lucas",
    "last_name": "Oliveira",
    "id_number": "2222",
    "gender": "M",
    "date_of_birth": "1998-01-13",
    "country_of_origin": "Brazil"
}' 
```
### POST team 
```
curl --request POST \
  --url http://localhost:8000/team/ \
  --header 'Content-Type: application/json' \
  --cookie csrftoken=rXrStS5ouDlC2I2GqL9DnIhjVGnwzdcZ \
  --data '{
    "members_id": [1],
    "name": "team test",
    "country_of_origin": "Brazil",
    "representative_name": "Lucas"
}'
```
### Remove participant (Put team). important, the ids that are placed in the members_id field replace ALL PARTICIPANTS and cam be empty
```
curl --request PATCH \
  --url http://localhost:8000/team/1/ \
  --header 'Content-Type: application/json' \
  --cookie csrftoken=rXrStS5ouDlC2I2GqL9DnIhjVGnwzdcZ \
  --data '{
    "members_id": []
}'
```

### POST competition
```
curl --request POST \
  --url http://localhost:8000/competition/ \
  --header 'Content-Type: application/json' \
  --cookie csrftoken=rXrStS5ouDlC2I2GqL9DnIhjVGnwzdcZ \
  --data '{
    "team": 1,
    "instance": "Local",
    "year": 2023,
    "score": 80
}'
```

### GET competitions
```
curl --request GET \
  --url 'http://localhost:8000/competition?year=2023&instance=Local' \
  --cookie csrftoken=rXrStS5ouDlC2I2GqL9DnIhjVGnwzdcZ
```
