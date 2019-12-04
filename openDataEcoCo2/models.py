from django.db import models

class Record(models.Model):
    recordid =  models.CharField(max_length=100, primary_key=True)
    date_heure = models.CharField(max_length=25)
    date = models.DateField()
    heure = models.TimeField()
    taux_co2 = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return self.date_heure
