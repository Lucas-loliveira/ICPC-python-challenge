from django.contrib import admin
from .models import Participant, Team, Competition

admin.site.register(Participant)
admin.site.register(Team)
admin.site.register(Competition)
