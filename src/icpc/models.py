from django.db import models


class Participant(models.Model):
    GENDER_CHOICES = (
        ("F", "Female"),
        ("M", "Male"),
    )

    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    id_number = models.CharField(max_length=30)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    date_of_birth = models.DateField()
    country_of_origin = models.CharField(max_length=300)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Team(models.Model):
    members = models.ManyToManyField(Participant)
    name = models.CharField(max_length=50)
    country_of_origin = models.CharField(max_length=50)
    representative_name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Competition(models.Model):
    INSTANCE_CHOICE = (
        ("00LO", "Local"),
        ("01NA", "National"),
        ("02RE", "Regional"),
        ("03IN", "International"),
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None)
    instance = models.CharField(choices=INSTANCE_CHOICE, max_length=4)
    year = models.IntegerField()
    score = models.IntegerField()

    class Meta:
        unique_together = ("team", "instance", "year")
