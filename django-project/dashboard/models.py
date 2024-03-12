from django.db import models
from django.contrib.auth.models import User

class Log(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    dstime = models.TimeField()
    detime = models.TimeField(blank=True)
    pstime = models.TimeField(blank=True)
    petime = models.TimeField(blank=True)
    notes = models.TextField(blank=True)