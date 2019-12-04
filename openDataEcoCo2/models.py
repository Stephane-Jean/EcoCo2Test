from django.db import models

class Record(models.Model):
    recordid =  models.CharField(max_length=100, primary_key=True)
    taux_co2 = models.IntegerField()
    date_heure = models.CharField(max_length=25)
    def __str__(self):
        return self.date_heure
