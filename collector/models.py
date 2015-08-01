from django.db import models

# Create your models here.

class HumidTemp(models.Model):
    temperature = models.FloatField()
    humidity = models.FloatField()
    collect_datetime = models.DateTimeField()

    def __str__(self):
        return str(self.temperature) + ', ' + str(self.humidity) + ', ' + str(self.collect_datetime)
