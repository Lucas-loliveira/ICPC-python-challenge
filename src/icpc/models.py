from django.db import models



class Participant(models.Model):
    GENDER_CHOICES = (
            ("F", "Female"),
            ("M", "Male"),
        )

    first_name = models.CharField(max_length = 300)
    last_name = models.CharField(max_length = 300)
    id_number = models.CharField(max_length = 30)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=1)
    date_of_birth = models.DateField()
    country_of_origin = models.CharField(max_length = 300)
    def __str__(self):
        return self.first_name + " " + self.last_name


class Team(models.Model):
    members = models.ManyToManyField(Participant)
    def __str__(self):
        return str(self.id)




class Competition(models.Model):
    INSTANCE_CHOICE = (
            ("LO", "Local"),
            ("NA", "National"),
            ("RE", "Regional"),
            ("IN", "International"),
        )
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default=None)
    instance =  models.CharField(choices=INSTANCE_CHOICE,max_length=2)
    year = models.IntegerField()
    score = models.IntegerField()
    

